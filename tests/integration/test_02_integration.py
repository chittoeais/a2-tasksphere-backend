import pytest


from tests.integration.conf_integration import _register, _login

@pytest.mark.anyio
async def test_integration_register_and_login(client):
    await _register(client, "flow2@example.com")
    login_response = await _login(client, "flow2@example.com")
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"