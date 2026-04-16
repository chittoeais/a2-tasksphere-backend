from fastapi import APIRouter, HTTPException, Request, status

from app.models.auth import UserRegister
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(payload: UserRegister, request: Request):
    users = request.app.database["users"]

    existing = await users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    await users.insert_one({
        "email": payload.email,
        "password_hash": hash_password(payload.password)
    })

    return {"message": "User registered successfully"}