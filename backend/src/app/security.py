from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.configs import SETTINGS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=SETTINGS.auth.access_token_expire_minutes
    )
    payload = {
        "sub": subject,
        "type": "access",
        "exp": expire,
    }
    return jwt.encode(
        payload,
        SETTINGS.auth.jwt_secret_key,
        algorithm=SETTINGS.auth.jwt_algorithm,
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        SETTINGS.auth.jwt_secret_key,
        algorithms=[SETTINGS.auth.jwt_algorithm],
    )
