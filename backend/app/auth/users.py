from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Store plain passwords temporarily for demo use
RAW_USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "analyst": {"password": "analyst123", "role": "analyst"},
    "viewer": {"password": "viewer123", "role": "viewer"},
}

def get_user(username: str) -> dict | None:
    user = RAW_USERS.get(username)
    if not user:
        return None
    # Hash only when needed
    return {
        "username": username,
        "password_hash": pwd_context.hash(user["password"][:72]),
        "role": user["role"],
    }

def verify_user(username: str, password: str) -> dict | None:
    user = get_user(username)
    if not user or not pwd_context.verify(password, user["password_hash"]):
        return None
    return {"username": username, "role": user["role"]}
