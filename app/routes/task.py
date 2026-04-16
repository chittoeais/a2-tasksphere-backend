from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request, Depends

from app.models.task import TaskCreate
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