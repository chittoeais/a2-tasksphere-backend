import pytest
from bson import ObjectId
from fastapi import HTTPException

from app.models.task import TaskUpdate
from app.routes import task as task_routes

@pytest.mark.anyio
async def test_update_task_updates_selected_fields(unit_request):
    tasks = unit_request.app.database["tasks"]
    inserted = await tasks.insert_one(
        {
            "title": "Initial",
            "description": "old",
            "status": "To Do",
            "owner_email": "owner@example.com",
        }
    )

    payload = TaskUpdate(title="Renamed", status="Completed")

    response = await task_routes.update_task(
        task_id=str(inserted.inserted_id),
        payload=payload,
        request=unit_request,
        user_email="owner@example.com",
    )

    assert response["title"] == "Renamed"
    assert response["status"] == "Completed"
    assert response["description"] == "old"


@pytest.mark.anyio
async def test_update_task_returns_404_when_task_missing_or_not_owned(unit_request):
    payload = TaskUpdate(title="Does not matter")

    with pytest.raises(HTTPException) as exc:
        await task_routes.update_task(
            task_id=str(ObjectId()),
            payload=payload,
            request=unit_request,
            user_email="owner@example.com",
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Task not found"