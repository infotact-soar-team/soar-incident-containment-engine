"""
Hardcoded demo users for now — real user management is out of scope
for this internship project. Passwords are bcrypt-hashed.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEMO_USERS = {
    "admin": {"password_hash": pwd_context.hash("admin123"), "role": "admin"},
    "analyst": {"password_hash": pwd_context.hash("analyst123"), "role": "analyst"},
    "viewer": {"password_hash": pwd_context.hash("viewer123"), "role": "viewer"},
}


def verify_user(username: str, password: str) -> dict:
    user = DEMO_USERS.get(username)
    if not user or not pwd_context.verify(password, user["password_hash"]):
        return None
    return {"username": username, "role": user["role"]}