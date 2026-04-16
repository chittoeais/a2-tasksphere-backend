import pytest
from bson import ObjectId

from app.routes import task as task_routes

@pytest.mark.anyio
async def test_list_tasks_returns_only_owner_tasks_in_desc_order(unit_request):
    tasks = unit_request.app.database["tasks"]

    await tasks.insert_one(
        {
            "_id": ObjectId("000000000000000000000001"),
            "title": "Older",
            "description": "older desc",
            "status": "To Do",
            "owner_email": "owner@example.com",
        }
    )
    await tasks.insert_one(
        {
            "_id": ObjectId("000000000000000000000002"),
            "title": "Newer",
            "description": "new desc",
            "status": "In Progress",
            "owner_email": "owner@example.com",
        }
    )
    await tasks.insert_one(
        {
            "_id": ObjectId("000000000000000000000003"),
            "title": "Other user",
            "description": "ignore",
            "status": "To Do",
            "owner_email": "other@example.com",
        }
    )

    response = await task_routes.list_tasks(request=unit_request, user_email="owner@example.com")

    assert [task["title"] for task in response] == ["Newer", "Older"]
    assert all(task["owner_email"] == "owner@example.com" for task in response)