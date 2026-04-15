from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request, Depends
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