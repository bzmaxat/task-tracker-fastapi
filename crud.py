from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
import models
import schemas
import auth


# PROJECT CRUD
async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 0):
    result = await db.execute(select(models.Project).options(selectinload(models.Project.tasks)).offset(skip).limit(limit))
    return result.scalars().all()


async def get_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(models.Project).options(joinedload(models.Project.tasks)).filter(models.Project.id == project_id))
    return result.scalars().first()


async def create_project(db: AsyncSession, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(name=project.name, description=project.description, owner_id=user_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def delete_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(models.Project).options(joinedload(models.Project.tasks)).filter(models.Project.id == project_id))
    db_project = result.scalars().first()
    if db_project:
        await db.delete(db_project)
        await db.commit()
    return db_project


# TASK CRUD
async def get_tasks(db: AsyncSession, project_id: int = None, completed: bool = None, owner_id: int = None, skip: int = 0, limit: int = 10):
    query = select(models.Task)

    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)

    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    if owner_id is not None:
        query = query.filter(models.Task.owner_id == owner_id)

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id))
    return result.scalars().first()


async def create_task(db: AsyncSession, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        project_id=task.project_id,
        owner_id=user_id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskBase):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id))
    db_task = result.scalars().first()

    if db_task:
        db_task.title = task_update.title
        db_task.description = task_update.description
        db_task.completed = task_update.completed
        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id))
    db_task = result.scalars().first()
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task


# USER CRUD
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    user = result.scalars().first()
    if user and auth.verify_password(password, user.hashed_password):
        return user
    return None
