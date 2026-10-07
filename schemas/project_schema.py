from schemas.task_schema import TaskRead, TaskCreate, TaskUpdate
from pydantic import Field
from models.project_model import ProjectBase, ProjectFullBase

class ProjectCreate(ProjectBase):
    tasks: list["TaskCreate"] | None = Field(default_factory=list)


class ProjectUpdate(ProjectBase):
    tasks: list["TaskUpdate"] | None = Field(default_factory=list)


class ProjectRead(ProjectFullBase):
    tasks: list["TaskRead"] | None = Field(default=[])
