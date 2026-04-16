import pytest


from tests.integration.conf_integration import _register, _login, _auth_headers

@pytest.mark.anyio
async def test_integration_register_login_logout(client):
    await _register(client, "flow8@example.com")
    token = (await _login(client, "flow8@example.com")).json()["access_token"]
    headers = _auth_headers(token)

    logout_response = await client.post("/auth/logout", headers=headers)
    assert logout_response.status_code == 200
    assert logout_response.json() == {"message": "Logged out successfully. Client should remove the token."}