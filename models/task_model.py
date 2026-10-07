from typing import TYPE_CHECKING
from sqlalchemy import orm
from sqlmodel import Field, Relationship, SQLModel
from models.base_model import BaseULIDModel

if TYPE_CHECKING:
    from models.project_model import Project


class TaskBase(SQLModel):
    title: str = Field(max_length=200)
    done: bool = False
    priority: str = Field(default="medium")
    project_id: str = Field(..., max_length=26)

class TaskFullBase(TaskBase, BaseULIDModel):
    pass


class Task(TaskFullBase, table=True):
    # project_id: str | None = Field(
    #     default=None,
    #     foreign_key="project.id",
    #     max_length=26,
    # )
    project: "Project" = Relationship(
        # back_populates="tasks",
        sa_relationship=orm.RelationshipProperty(
            "Project",
            lazy="select",
            viewonly=True,
            primaryjoin="Project.id == foreign(Task.project_id)"
        )
    )
