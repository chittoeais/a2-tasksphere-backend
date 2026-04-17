import pytest


from tests.integration.conf_integration import _register, _login, _auth_headers

@pytest.mark.anyio
async def test_integration_register_login_list_create_update_task(client):
    await _register(client, "flow5@example.com")
    token = (await _login(client, "flow5@example.com")).json()["access_token"]
    headers = _auth_headers(token)

    create_response = await client.post(
        "/tasks",
        headers=headers,
        json={"title": "Flow 5 task", "description": "first"},
    )
    task_id = create_response.json()["id"]

    update_response = await client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={"title": "Flow 5 updated", "status": "Completed"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Flow 5 updated"
    assert updated["status"] == "Completed"