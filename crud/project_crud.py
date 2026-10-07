from fastapi import HTTPException, status
from sqlalchemy import orm, select, delete, update

from crud.base_crud import CRUDBase
from models.project_model import Project
from models.task_model import Task, TaskFullBase
from schemas.project_schema import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_all_tasks_in_project(self) -> list[Project]:
        db_session = self.get_db().session
        query = select(Project).options(orm.selectinload(Project.tasks))
        result = await db_session.exec(query)
        return result.all()

    async def get_project_by_id_and_tasks(self, *, id=str) -> Project:
        db_session = self.get_db().session
        query = (
            select(Project)
            .where(Project.id == id)
            .options(orm.selectinload(Project.tasks))
        )
        result = await db_session.exec(query)
        return result.scalar_one_or_none()

    async def create_project_with_tasks(self, obj_in: ProjectCreate) -> Project:
        db_session = self.get_db().session
        try:
            project_data = obj_in.model_dump(exclude={"tasks"})
            project = await self.create(
                obj_in=project_data, db_session=db_session, with_commit=False
            )
            db_session.add(project)
            await db_session.flush()

            for task_in in obj_in.tasks or []:

                db_session.add(
                    Task(
                        project_id=project.id,
                        **task_in.model_dump(exclude={"project_id"}),
                    )
                )
                await db_session.flush()

            await db_session.commit()
            query = (
                select(Project)
                .where(Project.id == project.id)
                .options(orm.selectinload(Project.tasks))
            )
            result = await db_session.exec(query)
            return result.scalar_one()
        except Exception:
            await db_session.rollback()
            raise

    async def update_project_with_tasks(
        self,
        *,
        id: str,
        obj_in: ProjectUpdate,
    ) -> Project:
        db_session = self.get_db().session

        try:
            project = await self.get_project_by_id_and_tasks(id=id)

            if project is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project was not found!",
                )

            # Update project fields such as name.
            project_data = obj_in.model_dump(
                exclude_unset=True,
                exclude={"tasks"},
            )
            for field, value in project_data.items():
                setattr(project, field, value)

            # Only change tasks if the request included the "tasks" field.
            if "tasks" in obj_in.model_fields_set and obj_in.tasks is not None:
                existing_tasks = {
                    old_task.id: old_task for old_task in project.tasks
                }

                # Collect IDs the client supplied.
                incoming_ids = []
                for task_in in obj_in.tasks:
                    if task_in.id is not None:
                        incoming_ids.append(task_in.id)

                # Reject duplicate IDs.
                if len(incoming_ids) != len(set(incoming_ids)):
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="A task ID may only appear once.",
                    )

                incoming_id_set = set(incoming_ids)

                # Reject IDs that aren't tasks on this project.
                if not incoming_id_set.issubset(existing_tasks):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="One or more task IDs do not belong to this project.",
                    )

                # Create new tasks and update existing tasks.
                for task_in in obj_in.tasks:
                    new_data = task_in.model_dump(
                        exclude={"id", "project_id"},
                    )

                    if task_in.id is None:
                        db_session.add(
                            Task(
                                project_id=project.id,
                                **new_data,
                            )
                        )
                        continue

                    existing_task = existing_tasks[task_in.id]

                    old_data = {}
                    for field in new_data:
                        old_data[field] = getattr(existing_task, field)

                    if old_data != new_data:
                        for field, value in new_data.items():
                            setattr(existing_task, field, value)

                # Delete existing tasks omitted from the request.
                for old_id, old_task in existing_tasks.items():
                    if old_id not in incoming_id_set:
                        await db_session.delete(old_task)

            await db_session.commit()

            # Reload with tasks so FastAPI can serialize the response.
            query = (
                select(Project)
                .where(Project.id == project.id)
                .options(orm.selectinload(Project.tasks))
            )
            result = await db_session.exec(query)

            return result.scalar_one()

        except Exception:
            await db_session.rollback()
            raise


project = CRUDProject(Project)
