from pydantic import BaseModel, EmailStr
from typing import List


# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TaskCreate(TaskBase):
    project_id: int
    owner_id: int


class TaskResponse(TaskBase):
    id: int
    project_id: int
    owner_id: int

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
    owner_id: int
    tasks: List[TaskResponse] = []

    class Config:
        orm_mode = True


# User Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
