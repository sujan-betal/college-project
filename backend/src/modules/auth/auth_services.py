from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.concurrency import run_in_threadpool
import logging
import secrets

from src.models.user_model import User
from src.models.permission_model import UserPermission
from src.modules.auth.auth_schemas import LoginSchema
from src.utils.jwt import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
)
from src.utils.password import verify_password, hash_password
from src.utils.mailer import send_password_reset_email
from src.utils.common_schema import api_response_success, api_response_error
from src.utils.status_code import StatusCode

logger = logging.getLogger(__name__)


async def get_permissions(db: AsyncSession, userid: str):
    rows = (await db.execute(
        select(UserPermission.permission).where(UserPermission.userid == userid)
    )).scalars().all()

    return sorted({(code or "").upper() for code in rows})


async def login(db: AsyncSession, payload: LoginSchema):
    result = await db.execute(
        select(User).where(
            (User.username == payload.username) | (User.email == payload.username)
        )
    )

    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password):
        return api_response_error(
            message="Invalid username or password",
            status_code=StatusCode.unauthorized
        )

    if user.is_deleted:
        return api_response_error(
            message="Account is deleted",
            status_code=StatusCode.unauthorized
        )

    if str(user.status).upper() != "ACTIVE":
        return api_response_error(
            message="Account is inactive",
            status_code=StatusCode.forbidden
        )

    access_token = create_access_token(user.userid, user.role)
    refresh_token = create_refresh_token(user.userid, user.role)
    permissions = await get_permissions(db, user.userid)

    return api_response_success(
        data={
            "userid": str(user.userid),
            "username": user.username,
            "role": user.role,
            "permissions": permissions,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "is_reset": user.is_reset,
        },
        message="Login successful",
        status_code=StatusCode.success
    )


async def me(db: AsyncSession, user: User):
    return api_response_success(
        data={
            "userid": str(user.userid),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "permissions": await get_permissions(db, user.userid),
        },
        message="Profile fetched"
    )


async def change_password(db: AsyncSession, user: User, payload):
    if not verify_password(payload.current_password, user.password):
        return api_response_error(
            message="Current password is incorrect",
            status_code=StatusCode.badRequest
        )

    if payload.new_password != payload.confirm_password:
        return api_response_error(
            message="Passwords do not match",
            status_code=StatusCode.badRequest
        )

    user.password = hash_password(payload.new_password)
    user.is_reset = False

    await db.commit()

    return api_response_success(message="Password changed")


async def refresh(db: AsyncSession, refresh_token: str):
    if not refresh_token:
        return api_response_error(
            message="Refresh token required",
            status_code=StatusCode.badRequest
        )

    try:
        decoded = decode_token(refresh_token)
    except Exception:
        return api_response_error(
            message="Invalid or expired refresh token",
            status_code=StatusCode.unauthorized
        )

    if decoded.get("type") != "refresh":
        return api_response_error(
            message="Invalid token type",
            status_code=StatusCode.unauthorized
        )

    result = await db.execute(select(User).where(User.userid == decoded.get("userid")))
    user = result.scalar_one_or_none()

    if not user or user.is_deleted or str(user.status).upper() != "ACTIVE":
        return api_response_error(
            message="Account is not active",
            status_code=StatusCode.unauthorized
        )

    return api_response_success(
        data={
            "access_token": create_access_token(user.userid, user.role),
            "refresh_token": create_refresh_token(user.userid, user.role),
            "role": user.role,
        },
        message="Token refreshed",
    )


async def reset_password(db: AsyncSession, payload):
    if payload.new_password != payload.confirm_password:
        return api_response_error(
            message="Passwords do not match",
            status_code=StatusCode.badRequest
        )

    result = await db.execute(select(User).where(User.userid == payload.user_id))
    user = result.scalar_one_or_none()

    if not user or user.is_deleted:
        return api_response_error(
            message="User not found",
            status_code=StatusCode.notFound
        )

    user.password = hash_password(payload.new_password)
    user.is_reset = True

    await db.commit()

    return api_response_success(message="Password reset. User must set a new password on next login.")


def check_password_match(new_password: str, confirm_password: str):
    if new_password != confirm_password:
        return api_response_error(
            message="Passwords do not match",
            status_code=StatusCode.badRequest
        )

    if len(new_password) < 8:
        return api_response_error(
            message="Password must be at least 8 characters",
            status_code=StatusCode.badRequest
        )

    if new_password.isalpha() or new_password.isdigit():
        return api_response_error(
            message="Password must contain both letters and numbers",
            status_code=StatusCode.badRequest
        )

    return None


async def set_password_with_token(db: AsyncSession, payload):
    """
    Used from the link emailed to a new user. The token proves who they are,
    so no existing password is needed.
    """
    mismatch = check_password_match(payload.new_password, payload.confirm_password)
    if mismatch:
        return mismatch

    try:
        decoded = decode_token(payload.token)
    except Exception:
        return api_response_error(
            message="This link is invalid or has expired. Please ask for a new one.",
            status_code=StatusCode.unauthorized
        )

    if decoded.get("type") != "reset":
        return api_response_error(message="Invalid link", status_code=StatusCode.unauthorized)

    result = await db.execute(select(User).where(User.userid == decoded.get("userid")))
    user = result.scalar_one_or_none()

    if not user or user.is_deleted:
        return api_response_error(message="User not found", status_code=StatusCode.notFound)

    # Each emailed link works exactly once: the nonce is cleared on use.
    nonce = decoded.get("nonce") or ""
    if not nonce or not user.reset_nonce or nonce != user.reset_nonce:
        return api_response_error(
            message="This link has already been used. Please request a new one.",
            status_code=StatusCode.unauthorized
        )

    if str(user.status).upper() != "ACTIVE":
        return api_response_error(
            message="This account is inactive. Please contact the administrator.",
            status_code=StatusCode.forbidden
        )

    user.password = hash_password(payload.new_password)
    user.is_reset = False
    user.reset_nonce = None

    await db.commit()

    # Hand back a usable session so they land straight on their dashboard.
    return api_response_success(
        data={
            "userid": str(user.userid),
            "username": user.username,
            "role": user.role,
            "access_token": create_access_token(user.userid, user.role),
            "refresh_token": create_refresh_token(user.userid, user.role),
        },
        message="Password set. You are now signed in.",
    )


async def forgot_password(db: AsyncSession, payload):
    """
    Email a fresh reset link. Always answers success so the response cannot be
    used to discover which emails exist.
    """
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalar_one_or_none()

    generic = api_response_success(
        message="If that email is registered, a reset link is on its way."
    )

    if not user or user.is_deleted or str(user.status).upper() != "ACTIVE":
        return generic

    nonce = secrets.token_urlsafe(24)
    user.reset_nonce = nonce
    await db.commit()

    token = create_reset_token(user.userid, user.role, nonce)
    sent, error = await run_in_threadpool(
        send_password_reset_email, user.email, user.username, token
    )

    if not sent:
        logger.warning("Forgot-password email failed: %s", error)

    return generic