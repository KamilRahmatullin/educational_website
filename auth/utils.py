from datetime import timedelta, datetime

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
        payload: dict,
        key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
) -> str:
    """
    Encodes a JWT token with the provided payload and optional expiration time.
    """
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload, key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    """
    Decodes a JWT token with the provided public key and algorithm
    """
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    This function generates a salt using bcrypt.gensalt(), encodes the password to bytes,
    and then uses bcrypt.hashpw() to hash the password with the generated salt.
    The hashed password is returned as bytes.
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password=hashed_password)
