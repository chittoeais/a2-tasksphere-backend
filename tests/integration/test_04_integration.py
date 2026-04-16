import pytest


from tests.integration.conf_integration import _register, _login, _auth_headers

@pytest.mark.anyio
async def test_integration_register_login_list_tasks(client):
    await _register(client, "flow3@example.com")
    token = (await _login(client, "flow3@example.com")).json()["access_token"]
    headers = _auth_headers(token)

    list_response = await client.get("/tasks", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json() == []