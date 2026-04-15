from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

TaskStatus = Literal["To Do", "In Progress", "Completed"]