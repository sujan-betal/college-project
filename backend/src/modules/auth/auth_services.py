from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config.database import SessionLocal
from src.models.user_model import User
from src.models.permission_model import UserPermission, Permission
from src.modules.auth.auth_schemas import LoginSchema
from src.utils.jwt import create_access_token, create_refresh_token
from src.utils.password import verify_password
from src.utils.common_schema import api_response_success, api_response_error
from src.utils.status_code import StatusCode


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

    return api_response_success(
        data={
            "userid": str(user.userid),
            "username": user.username,
            "role": user.role,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "is_reset": user.is_reset
        },
        message="Login successful",
        status_code=StatusCode.success
    )


async def get_permissions(db: AsyncSession, userid: str):
    result = await db.execute(
        select(Permission.code)
        .join(UserPermission, UserPermission.permissionid == Permission.id)
        .where(UserPermission.userid == userid)
    )

    return [code for code in result.scalars().all()]


async def me(db: AsyncSession, user: User):
    permissions = await get_permissions(db, user.userid)

    if str(user.role).upper() == "SUPER_ADMIN":
        permissions = ["ALL"]

    return api_response_success(
        data={
            "userid": str(user.userid),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "permissions": permissions
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

    from src.utils.password import hash_password

    user.password = hash_password(payload.new_password)
    user.is_reset = False

    await db.commit()

    return api_response_success(message="Password changed")