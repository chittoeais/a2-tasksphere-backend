from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request, Depends

from app.models.task import TaskCreate, TaskUpdate
from app.auth import get_current_user_email

router = APIRouter(prefix="/tasks", tags=["tasks"])

def task_doc_to_dict(doc):
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc.get("description"),
        "status": doc["status"],
        "owner_email": doc["owner_email"]
    }

@router.get("")
async def list_tasks(request: Request, user_email: str = Depends(get_current_user_email)):
    tasks = request.app.database["tasks"]
    results = []
    async for doc in tasks.find({"owner_email": user_email}).sort("_id", -1):
        results.append(task_doc_to_dict(doc))
    return results

@router.post("")
async def create_task(payload: TaskCreate, request: Request, user_email: str = Depends(get_current_user_email)):
    tasks = request.app.database["tasks"]
    doc = {
        "title": payload.title,
        "description": payload.description,
        "status": "To Do",
        "owner_email": user_email
    }
    result = await tasks.insert_one(doc)
    created = await tasks.find_one({"_id": result.inserted_id})
    return task_doc_to_dict(created)

@router.put("/{task_id}")
async def update_task(task_id: str, payload: TaskUpdate, request: Request, user_email: str = Depends(get_current_user_email)):
    tasks = request.app.database["tasks"]

    existing = await tasks.find_one({"_id": ObjectId(task_id), "owner_email": user_email})
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = {}
    if payload.title is not None:
        update_data["title"] = payload.title
    if payload.description is not None:
        update_data["description"] = payload.description
    if payload.status is not None:
        update_data["status"] = payload.status

    await tasks.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    updated = await tasks.find_one({"_id": ObjectId(task_id)})
    return task_doc_to_dict(updated)