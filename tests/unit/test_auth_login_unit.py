import pytest
from fastapi import HTTPException

from app.models.auth import UserLogin
from app.routes import auth as auth_routes

@pytest.mark.anyio
async def test_login_returns_access_token_on_valid_credentials(unit_request, monkeypatch):
    users = unit_request.app.database["users"]
    await users.insert_one({"email": "login@example.com", "password_hash": "stored-hash"})

    monkeypatch.setattr(auth_routes, "verify_password", lambda raw, stored: raw == "StrongPass1!" and stored == "stored-hash")
    monkeypatch.setattr(auth_routes, "create_access_token", lambda subject: f"token::{subject}")

    payload = UserLogin(email="login@example.com", password="StrongPass1!")
    response = await auth_routes.login(payload=payload, request=unit_request)

    assert response.access_token == "token::login@example.com"
    assert response.token_type == "bearer"


@pytest.mark.anyio
async def test_login_rejects_invalid_credentials(unit_request, monkeypatch):
    users = unit_request.app.database["users"]
    await users.insert_one({"email": "login@example.com", "password_hash": "stored-hash"})

    monkeypatch.setattr(auth_routes, "verify_password", lambda *_: False)

    payload = UserLogin(email="login@example.com", password="WrongPassword")

    with pytest.raises(HTTPException) as exc:
        await auth_routes.login(payload=payload, request=unit_request)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid credentials"