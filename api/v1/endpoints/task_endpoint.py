from fastapi import APIRouter, HTTPException, status, Query

import crud
from models.task_model import Task
from schemas.task_schema import TaskRead, TaskCreate, TaskUpdate
from schemas.response_schema import GetResponseBaseSchema, PostResponseSchema, PutResponseSchema, DeleteResponseSchema, create_response

router = APIRouter()

@router.get("unfinished", response_model=GetResponseBaseSchema[list[TaskRead]])
async def get_unfinished_task():
    tasks: list[Task] =  await crud.task.get_unfinished_tasks()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No unfinished tasks found")

    return create_response(data=tasks)

@router.get("",response_model=GetResponseBaseSchema[list[TaskRead]])
async def get_all_tasks(priority: str |None = Query(default=None)):
    if priority is None:
        tasks: list[Task] = await crud.task.get_multi()
    else:
        tasks: list
    return create_response(data=tasks)

@router.get("{id}", response_model=GetResponseBaseSchema[TaskRead])
async def get_task_by_id(id:str):
    task: Task = await crud.task.get(id=id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return create_response(data=task)

@router.post("", response_model=PostResponseSchema[TaskRead], status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreate):
    task: Task = await crud.task.create(obj_in=task_create)
    return create_response(data=task, message="Task created successfully")

@router.put("{id}", response_model=PutResponseSchema[TaskRead])
async def update_task(id:str, task_update: TaskUpdate):
    task: Task = await crud.task.get(id=id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task: Task = await crud.task.update(obj_current=task, obj_new=task_update)
    return create_response(data=updated_task, message="Task updated successfully")

@router.delete("{id}", response_model=DeleteResponseSchema[TaskRead])
async def delete_task(id:str):
    task: Task = await crud.task.get(id=id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    deleted_task: Task = await crud.task.remove(id=id)
    return create_response(data=deleted_task, message="Task deleted successfully")

@router.get("{project_id}/tasks", response_model=GetResponseBaseSchema[TaskRead])
async def get_tasks_by_project_id(project_id: str):
    task: Task = await crud.task.get_tasks_by_project_id(project_id=project_id) 
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, message="Task not found")
    return create_response(data=task)
