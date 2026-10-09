from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from src.config.settings import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_MINUTES,
    REFRESH_TOKEN_DAYS,
    RESET_TOKEN_MINUTES,
)


def create_access_token(userid: str, role: str) -> str:
    payload = {
        "userid": userid,
        "role": role,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(userid: str, role: str) -> str:
    payload = {
        "userid": userid,
        "role": role,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_reset_token(userid: str, role: str = "", nonce: str = "") -> str:
    """Short lived, single-use token emailed to a new user."""
    payload = {
        "userid": userid,
        "role": role,
        "nonce": nonce,
        "type": "reset",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def verify_token(token: str) -> bool:
    try:
        decode_token(token)
        return True
    except JWTError:
        return False