from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import models
from database import engine, SessionLocal
import schemas
import crud
from models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

# OAuth2PasswordBearer token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PROTECTED ROUTE (Requires JWT)
@app.get("/users/me/", response_model=schemas.UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# PROJECT ROUTES
# Create Project (Authenticated User Only)
@app.post("/projects/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_project(db, project, user.id)


@app.get("/projects/", response_model=list[schemas.ProjectResponse])
def get_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.delete_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


# TASK ROUTES
# Create Task (Authenticated User Only)
@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_task(db, task, user.id)


@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskBase, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


# REGISTER USER
@app.post("/register/", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db, user)


# LOGIN (Generate JWT Token)
@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}





















