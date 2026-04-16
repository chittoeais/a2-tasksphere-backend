import pytest

from app.routes import auth as auth_routes

@pytest.mark.anyio
async def test_logout_returns_expected_message():
    response = await auth_routes.logout(user_email="owner@example.com")

    assert response == {"message": "Logged out successfully. Client should remove the token."}