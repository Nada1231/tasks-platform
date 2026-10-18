from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Task


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Crée les tables au démarrage (suffisant pour ce projet ; en prod : migrations Alembic)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Tasks API", lifespan=lifespan)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    done: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(Task).order_by(Task.id)).all()


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=payload.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
