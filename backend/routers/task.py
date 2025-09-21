from typing import Annotated

from pydantic import NonNegativeInt
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from db.database import get_db
from models.task import Task, TaskStatus
from schemas.task import TaskResponse, TaskCreateRequest, PreviewTaskResponse, TaskUpdateRequest


task_router = APIRouter(prefix="/tasks")


@task_router.post("/create")
def create_task(
    request: TaskCreateRequest,
    db: Annotated[Session, Depends(get_db)]
) -> TaskResponse:
    task = Task(**request.model_dump(), status=TaskStatus.PLANNED)    
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@task_router.get("/search")
def search_tasks(
    page_index: NonNegativeInt,
    page_size: NonNegativeInt,
    search_term: str,
    db: Annotated[Session, Depends(get_db)]
) -> list[PreviewTaskResponse]:
    wildcarded_query = f"%{search_term}%"
    stmt = (
        select(Task)
        .where(
            or_(
                Task.title.ilike(wildcarded_query),
                Task.description.ilike(wildcarded_query)
            )
        )
        .offset(page_size * page_index)
        .limit(page_size)
    )

    return db.scalars(stmt)


@task_router.get("/{id}")
def get_task_by_id(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> TaskResponse:
    task = db.get(Task, id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks found for the given id"
        )
    
    return task


@task_router.delete("/{id}")
def delete_task(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> TaskResponse:
    task = db.get(Task, id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks found for the given id"            
        )
    
    response = TaskResponse.model_validate(task)
    db.delete(task)
    db.commit()

    return response


@task_router.put("/{id}")
def update_task(
    id: int,
    request: TaskUpdateRequest,
    db: Annotated[Session, Depends(get_db)]
):
    task = db.get(Task, id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks found for the given id"            
        )
    
    attrs_to_update = request.model_dump(exclude_unset=True)
    for key, value in attrs_to_update.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    
    return task


@task_router.get("/")
def get_tasks(
    page_index: NonNegativeInt,
    page_size: NonNegativeInt,
    db: Annotated[Session, Depends(get_db)]
) -> list[PreviewTaskResponse]:
    stmt = (
        select(Task)
        .offset(page_index * page_size)
        .limit(page_size)
    )

    return db.scalars(stmt)
