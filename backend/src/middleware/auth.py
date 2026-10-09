from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
import logging

from src.config.database import get_db
from src.models.user_model import User
from src.models.permission_model import UserPermission, Role

load_dotenv()

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

security = HTTPBearer()


def authorization(allowed_roles: list = None, required_permissions: list = None, require_admin_role: bool = False):
    allowed_roles = allowed_roles or []
    required_permissions = [p.upper() for p in (required_permissions or [])]

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
                decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )

            # --------------------------------------------------
            # 4. Extract userid and role
            # --------------------------------------------------

            userid = decoded.get("userid") or decoded.get("user_id")
            role = (decoded.get("role") or "").upper()

            if not userid or not role:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )

            # --------------------------------------------------
            # 5. Check Allowed Roles (validated against DB below)
            # --------------------------------------------------

            if allowed_roles and role not in [r.upper() for r in allowed_roles]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: invalid role"
                )

            # --------------------------------------------------
            # 6. Find User
            # --------------------------------------------------

            result = await db.execute(select(User).where(User.userid == userid))
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
            # 10. Validate the role exists and check admin access
            # --------------------------------------------------

            role_row = (await db.execute(
                select(Role).where(func.upper(Role.name) == role)
            )).scalar_one_or_none()

            if not role_row:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid role"
                )

            if require_admin_role and not role_row.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: role cannot access admin"
                )

            # --------------------------------------------------
            # 11. Load granted permissions
            # --------------------------------------------------

            permissions = {
                (code or "").upper()
                for code in (await db.execute(
                    select(UserPermission.permission).where(UserPermission.userid == existing_user.userid)
                )).scalars().all()
            }

            # --------------------------------------------------
            # 12. "ALL" grants everything
            # --------------------------------------------------

            if "ALL" in permissions:
                return existing_user

            # --------------------------------------------------
            # 13. Check required permissions
            # --------------------------------------------------

            if required_permissions:
                missing = [p for p in required_permissions if p not in permissions]

                if missing:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access denied: missing permission {missing[0]}"
                    )

            # --------------------------------------------------
            # 14. Authorized
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