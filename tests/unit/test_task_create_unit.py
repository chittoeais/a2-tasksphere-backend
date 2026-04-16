import pytest

from app.models.task import TaskCreate
from app.routes import task as task_routes

@pytest.mark.anyio
async def test_create_task_sets_default_status_and_owner(unit_request):
    payload = TaskCreate(title="Write tests", description="unit + integration")

    response = await task_routes.create_task(payload=payload, request=unit_request, user_email="owner@example.com")

    assert response["title"] == "Write tests"
    assert response["description"] == "unit + integration"
    assert response["status"] == "To Do"
    assert response["owner_email"] == "owner@example.com"

@pytest.mark.anyio
async def test_create_task_sets_default_status_and_owner1(unit_request):
    payload = TaskCreate(title="Write tests", description="unit + integration")

    response = await task_routes.create_task(payload=payload, request=unit_request, user_email="owner@example.com")

    assert response["title"] == "Write tests"
    assert response["description"] == "unit + integration"
    assert response["status"] == "To Do"
    assert response["owner_email"] == "owner@example.com"