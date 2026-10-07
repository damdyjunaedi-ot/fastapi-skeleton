from models.task_model import TaskBase, TaskFullBase
from pydantic import Field


class TaskCreate(TaskBase):
    project_id: str | None = None

class TaskUpdate(TaskBase):
    id: str | None = None
    project_id: str | None = None

class TaskRead(TaskFullBase):
    project_id: str | None = None
