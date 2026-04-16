import pytest
from fastapi import HTTPException

from app.models.auth import UserRegister
from app.routes import auth as auth_routes

@pytest.mark.anyio
async def test_register_creates_user_with_hashed_password(unit_request, monkeypatch):
    monkeypatch.setattr(auth_routes, "hash_password", lambda raw: f"hashed::{raw}")

    payload = UserRegister(email="unit@example.com", password="StrongPass1!")
    response = await auth_routes.register(payload=payload, request=unit_request)

    assert response == {"message": "User registered successfully"}

    created_user = await unit_request.app.database["users"].find_one({"email": payload.email})
    assert created_user is not None
    assert created_user["password_hash"] == "hashed::StrongPass1!"


@pytest.mark.anyio
async def test_register_rejects_duplicate_email(unit_request):
    users = unit_request.app.database["users"]
    await users.insert_one({"email": "duplicate@example.com", "password_hash": "x"})

    payload = UserRegister(email="duplicate@example.com", password="StrongPass1!")

    with pytest.raises(HTTPException) as exc:
        await auth_routes.register(payload=payload, request=unit_request)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already registered"

@pytest.mark.anyio
async def test_register_rejects_duplicated_email(unit_request):
    users = unit_request.app.database["users"]
    await users.insert_one({"email": "duplicate@example.com", "password_hash": "x"})

    payload = UserRegister(email="duplicate@example.com", password="StrongPass1!")

    with pytest.raises(HTTPException) as exc:
        await auth_routes.register(payload=payload, request=unit_request)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already registered"