from pydantic import BaseModel
from typing import List


# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TaskCreate(TaskBase):
    project_id: int


class TaskResponse(TaskBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True


# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    tasks: List[TaskResponse] = []

    class Config:
        orm_mode = True
