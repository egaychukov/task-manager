from datetime import datetime

from pydantic import BaseModel, field_validator

from models.task import TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class PreviewTaskResponse(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = None


class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

    @field_validator("title")
    @classmethod
    def check_title(cls, title: str) -> str:
        if title is None:
            raise ValueError(
                "title cannot be explicitly set to None"
            )
        
        return title

    @field_validator("status")
    @classmethod
    def check_status(cls, status: str) -> str:
        if status is None:
            raise ValueError(
                "status cannot be explicitly set to None"
            )
        
        return status
