from fastapi import APIRouter, HTTPException, Request, status
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])