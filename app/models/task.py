from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

TaskStatus = Literal["To Do", "In Progress", "Completed"]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)