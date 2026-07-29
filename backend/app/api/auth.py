from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.users import verify_user
from app.auth.jwt_handler import create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/auth/login")
def login(payload: LoginRequest):
    user = verify_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user["username"], user["role"])
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}