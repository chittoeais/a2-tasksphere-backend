import pytest


from tests.integration.conf_integration import _register

@pytest.mark.anyio
async def test_integration_register_only(client):
    response = await _register(client, "flow1@example.com")
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}