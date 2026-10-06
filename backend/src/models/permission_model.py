from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from src.config.base import Base


class Permission(Base):

    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String(100),
        unique=True,
        nullable=False
    )

    module = Column(
        String(50),
        nullable=False
    )

    action = Column(
        String(50),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    grants = relationship("UserPermission", back_populates="permission", cascade="all, delete-orphan")


class UserPermission(Base):

    __tablename__ = "user_permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    permissionid = Column(
        Integer,
        ForeignKey("permissions.id"),
        nullable=False
    )

    userid = Column(
        String(36),
        ForeignKey("users.userid"),
        nullable=False
    )

    granted_by = Column(
        String(36),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    permission = relationship("Permission", back_populates="grants")
    user = relationship("User", back_populates="permissions")


class RoleTemplate(Base):

    __tablename__ = "role_templates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    templateid = Column(
        String(36),
        default=lambda: str(uuid.uuid4()),
        server_default=text("(UUID())"),
        unique=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )