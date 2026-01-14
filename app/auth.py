from datetime import datetime, timedelta
from jose import jwt, JWTError
import hashlib

SECRET_KEY = "change_this_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


FAKE_USER = {
    "username": "admin",
    "password_hash": hash_password("admin123")
}


def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed


def authenticate(username: str, password: str):
    if username != FAKE_USER["username"]:
        return False
    if not verify_password(password, FAKE_USER["password_hash"]):
        return False
    return {"username": username}


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
