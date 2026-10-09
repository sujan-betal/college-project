from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.middleware.auth import authorization
from src.modules.auth.auth_schemas import (
    LoginSchema,
    ChangePasswordSchema,
    RefreshTokenSchema,
    ResetPasswordSchema,
    SetPasswordSchema,
    ForgotPasswordSchema,
)
from src.modules.auth import auth_services

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login")
async def user_login(payload: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await auth_services.login(db, payload)


@router.get("/me")
async def current_user(
    db: AsyncSession = Depends(get_db),
    user=Depends(authorization(allowed_roles=["STUDENT", "TEACHER", "ADMIN"]))
):
    return await auth_services.me(db, user)


@router.put("/password/change")
async def password_change(
    payload: ChangePasswordSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(authorization(allowed_roles=["STUDENT", "TEACHER", "ADMIN"]))
):
    return await auth_services.change_password(db, user, payload)


@router.post("/refresh")
async def refresh_token(payload: RefreshTokenSchema, db: AsyncSession = Depends(get_db)):
    return await auth_services.refresh(db, payload.refresh_token)


@router.post("/set-password")
async def set_password(payload: SetPasswordSchema, db: AsyncSession = Depends(get_db)):
    return await auth_services.set_password_with_token(db, payload)


@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordSchema, db: AsyncSession = Depends(get_db)):
    return await auth_services.forgot_password(db, payload)


@router.post("/reset")
async def reset(
    payload: ResetPasswordSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(authorization(allowed_roles=["ADMIN"]))
):
    return await auth_services.reset_password(db, payload)


@router.post("/logout")
async def logout():
    return {"success": True, "message": "Logged out"}