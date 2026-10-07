from typing import TYPE_CHECKING

from sqlalchemy import orm
from sqlmodel import Field, Relationship, SQLModel
from models.base_model import BaseULIDModel

# if TYPE_CHECKING:
from models.task_model import Task

class ProjectBase(SQLModel):
    name: str = Field(max_length=200)

class ProjectFullBase(ProjectBase, BaseULIDModel):
    pass

class Project(ProjectFullBase, table=True):
    tasks: list["Task"] = Relationship(
        sa_relationship=orm.RelationshipProperty(
            "Task",
            lazy="select",
            viewonly=True,
            primaryjoin="Project.id == foreign(Task.project_id)"
        )
    )