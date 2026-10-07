from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy import select, orm
from fastapi_pagination import Params
import crud
from models.project_model import Project
from schemas.project_schema import ProjectRead, ProjectCreate, ProjectUpdate
from deps.internal_key_deps import require_internal_keys
from schemas.response_schema import (
    GetResponseBaseSchema,
    GetResponsePaginatedSchema,
    PostResponseSchema,
    PutResponseSchema,
    DeleteResponseSchema,
    create_response,
)

router = APIRouter()


@router.get("", response_model=GetResponsePaginatedSchema[ProjectRead])
async def get_all_projects(params: Params = Depends()):
    query = select(Project).options(orm.selectinload(Project.tasks))
    projects: Project = await crud.project.get_multi_paginated(
        params=params, query=query
    )
    return create_response(data=projects)

@router.get("/{id}", response_model=GetResponseBaseSchema[ProjectRead])
async def get_project_by_id(id:str):
    project: Project = await crud.project.get_project_by_id_and_tasks(id=id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project id: {id} was not found!"
        )
    return create_response(data=project)

@router.post("", response_model=PostResponseSchema[ProjectCreate])
async def create_project(project_create: ProjectCreate):
    project: Project = await crud.project.create_project_with_tasks(
        obj_in=project_create
    )
    return create_response(data=project, message="Project created successfully!")


@router.put("/{id}", response_model=PutResponseSchema[ProjectRead])
async def update_project(id: str, project_update: ProjectUpdate):
    # project: Project = await crud.project.get(id=id)
    # if not project:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, message="Project was not found"
    #     )

    # updated_project: Project = await crud.project.update(
    #     obj_current=project, obj_new=project_update
    # )
    updated_project: Project = await crud.project.update_project_with_tasks(
        id=id, obj_in=project_update
    )
    return create_response(
        data=updated_project, message="Project updated successfully!"
    )


@router.delete("/{id}", response_model=DeleteResponseSchema[ProjectRead])
async def delete_project(id: str):
    project: Project = await crud.project.get(id=id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, message="Project was not found"
        )
    deleted_project: Project = await crud.project.remove(id=id)
    return create_response(
        data=deleted_project, message="Project deleted successfully!"
    )


@router.get("/health")
async def check_health():
    return {"message": "connected to server"}
