from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
import logging

from src.config.database import get_db
from src.models.user_model import User
from src.models.permission_model import UserPermission, Permission

load_dotenv()

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

security = HTTPBearer()


def authorization(
    allowed_roles: list = None,
    required_permissions: list = None
):
    allowed_roles = allowed_roles or []
    required_permissions = required_permissions or []

    async def authorize_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
    ):
        try:

            # --------------------------------------------------
            # 1. JWT Configuration
            # --------------------------------------------------

            if not SECRET_KEY or not ALGORITHM:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="JWT configuration missing"
                )

            # --------------------------------------------------
            # 2. Get Token
            # --------------------------------------------------

            token = credentials.credentials

            # --------------------------------------------------
            # 3. Decode Token
            # --------------------------------------------------

            try:
                decoded = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM]
                )

            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )

            # --------------------------------------------------
            # 4. Get userid and role from JWT
            # --------------------------------------------------

            userid = decoded.get("userid") or decoded.get("user_id")
            role = (decoded.get("role") or "").upper()

            if not userid or not role:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )

            # --------------------------------------------------
            # 5. Check Allowed Roles
            # --------------------------------------------------

            if allowed_roles:

                allowed = [
                    r.upper()
                    for r in allowed_roles
                ]

                if role not in allowed:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied: invalid role"
                    )

            if role not in ("STUDENT", "TEACHER", "SUB_ADMIN", "SUPER_ADMIN"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid role"
                )

            # --------------------------------------------------
            # 6. Find User by userid
            # --------------------------------------------------

            result = await db.execute(
                select(User).where(
                    User.userid == userid
                )
            )

            existing_user = result.scalar_one_or_none()

            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            # --------------------------------------------------
            # 7. Verify Role
            # --------------------------------------------------

            if str(existing_user.role).upper() != role:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid user role"
                )

            # --------------------------------------------------
            # 8. Check Deleted Account
            # --------------------------------------------------

            if existing_user.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is deleted"
                )

            # --------------------------------------------------
            # 9. Check Account Status
            # --------------------------------------------------

            if str(existing_user.status).upper() != "ACTIVE":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is inactive"
                )

            # --------------------------------------------------
            # 10. Super Admin bypasses permission checks
            # --------------------------------------------------

            if role == "SUPER_ADMIN":
                return existing_user

            # --------------------------------------------------
            # 11. Get Permissions
            # --------------------------------------------------

            perm_result = await db.execute(
                select(Permission.code)
                .join(UserPermission, UserPermission.permissionid == Permission.id)
                .where(UserPermission.userid == existing_user.userid)
            )

            permissions = [
                (code or "").upper()
                for code in perm_result.scalars().all()
            ]

            if "ALL" in permissions:
                return existing_user

            # --------------------------------------------------
            # 12. Required Permissions
            # --------------------------------------------------

            if required_permissions:

                has_permissions = all(
                    permission.upper() in permissions
                    for permission in required_permissions
                )

                if not has_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied: insufficient permissions"
                    )

            # --------------------------------------------------
            # 13. Authorized
            # --------------------------------------------------

            return existing_user

        except HTTPException:
            raise

        except Exception:

            logger.exception("AUTH ERROR")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    return authorize_user