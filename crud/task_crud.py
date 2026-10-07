from sqlmodel import select

from crud.base_crud import CRUDBase
from models.task_model import Task
from schemas.task_schema import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def get_unfinished_tasks(self) -> list[Task]:
        db_session = self.get_db().session

        query = select(Task).where(Task.done.is_(False))
        result = await db_session.exec(query)
        return result.all()   

    async def get_tasks_by_project_id(self, *, project_id:str)-> list[Task]:
        db_session = self.get_db().session

        query = select(Task).where(task.project_id == project_id)
        result = await db_session.exec(query)
        return result.all()



task = CRUDTask(Task)
