import pytest


from tests.integration.conf_integration import _register, _login, _auth_headers

@pytest.mark.anyio
async def test_integration_register_login_list_create_task(client):
    await _register(client, "flow4@example.com")
    token = (await _login(client, "flow4@example.com")).json()["access_token"]
    headers = _auth_headers(token)

    list_before = await client.get("/tasks", headers=headers)
    assert list_before.status_code == 200
    assert list_before.json() == []

    create_response = await client.post(
        "/tasks",
        headers=headers,
        json={"title": "Flow 4 task", "description": "first"},
    )
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["title"] == "Flow 4 task"
    assert created["description"] == "first"
    assert created["status"] == "To Do"

    list_after = await client.get("/tasks", headers=headers)
    assert list_after.status_code == 200
    assert [task["id"] for task in list_after.json()] == [created["id"]]