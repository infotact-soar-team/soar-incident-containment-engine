from fastapi import Depends, HTTPException, Header
from app.auth.jwt_handler import decode_access_token
from app.core.roles import Role, has_permission


def get_current_user(authorization: str = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return {"username": payload["sub"], "role": payload["role"]}


def require_permission(permission: str):
    def checker(user: dict = Depends(get_current_user)) -> dict:
        role = Role(user["role"])
        if not has_permission(role, permission):
            raise HTTPException(status_code=403, detail=f"Role '{role.value}' lacks permission '{permission}'")
        return user
    return checker
