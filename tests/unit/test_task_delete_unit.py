import pytest
from fastapi import HTTPException

from app.routes import task as task_routes

@pytest.mark.anyio
async def test_delete_task_removes_task_for_owner(unit_request):
    tasks = unit_request.app.database["tasks"]
    inserted = await tasks.insert_one(
        {
            "title": "Delete me",
            "description": None,
            "status": "To Do",
            "owner_email": "owner@example.com",
        }
    )

    response = await task_routes.delete_task(
        task_id=str(inserted.inserted_id),
        request=unit_request,
        user_email="owner@example.com",
    )

    assert response == {"message": "Task deleted successfully"}
    assert await tasks.find_one({"_id": inserted.inserted_id}) is None


@pytest.mark.anyio
async def test_delete_task_returns_404_when_not_owned(unit_request):
    tasks = unit_request.app.database["tasks"]
    inserted = await tasks.insert_one(
        {
            "title": "Protected",
            "description": None,
            "status": "To Do",
            "owner_email": "other@example.com",
        }
    )

    with pytest.raises(HTTPException) as exc:
        await task_routes.delete_task(
            task_id=str(inserted.inserted_id),
            request=unit_request,
            user_email="owner@example.com",
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Task not found"