from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user_model import User
from src.models.permission_model import Permission, UserPermission
from src.modules.auth.auth_schemas import LoginSchema
from src.utils.jwt import create_access_token, create_refresh_token, decode_token
from src.utils.password import verify_password, hash_password
from src.utils.common_schema import api_response_success, api_response_error
from src.utils.status_code import StatusCode


async def get_permissions(db: AsyncSession, userid: str):
    rows = (await db.execute(
        select(Permission.code)
        .join(UserPermission, UserPermission.permissionid == Permission.id)
        .where(UserPermission.userid == userid)
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