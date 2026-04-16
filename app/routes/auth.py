from fastapi import APIRouter, HTTPException, Request, status

from app.models.auth import UserRegister, UserLogin, TokenResponse
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

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, request: Request):
    users = request.app.database["users"]

    user = await users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(payload.email)
    return TokenResponse(access_token=token)