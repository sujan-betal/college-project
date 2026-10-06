from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.middleware.auth import authorization
from src.modules.auth.auth_schemas import LoginSchema, ChangePasswordSchema
from src.modules.auth.auth_services import login, me, change_password

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login")
async def user_login(payload: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await login(db, payload)


@router.get("/me")
async def current_user(
    db: AsyncSession = Depends(get_db),
    user=Depends(authorization(allowed_roles=["STUDENT", "TEACHER", "SUB_ADMIN", "SUPER_ADMIN"]))
):
    return await me(db, user)


@router.put("/password/change")
async def password_change(
    payload: ChangePasswordSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(authorization(allowed_roles=["STUDENT", "TEACHER", "SUB_ADMIN", "SUPER_ADMIN"]))
):
    return await change_password(db, user, payload)


@router.post("/logout")
async def logout():
    return {"success": True, "message": "Logged out"}