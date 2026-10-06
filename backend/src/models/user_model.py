from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from src.config.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(150),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True
    )

    password = Column(
        Text,
        nullable=False
    )

    role = Column(
        String(30),
        default="STUDENT"
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )

    is_reset = Column(
        Boolean,
        default=True,
        server_default="1",
        nullable=False
    )

    is_deleted = Column(
        Boolean,
        default=False,
        server_default="0",
        nullable=False
    )

    userid = Column(
        String(36),
        default=lambda: str(uuid.uuid4()),
        server_default=text("(UUID())"),
        unique=True,
        nullable=False
    )

    created_by = Column(
        String(36),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    permissions = relationship("UserPermission", back_populates="user", cascade="all, delete-orphan")
    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)