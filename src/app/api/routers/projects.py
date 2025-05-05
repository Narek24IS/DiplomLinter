from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db import crud, schemas, connection

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=schemas.Project)
def create_project(
        project: schemas.ProjectCreate,
        db: Session = Depends(connection.get_db)
):
    token = project.token
    owner = crud.get_user_by_token(db, token=token)
    if not owner:
        raise HTTPException(status_code=403, detail="User not found")
    db_project = crud.get_project_by_name(db, project_name=project.name)
    if db_project:
        raise HTTPException(status_code=400, detail="Project already exists")
    return crud.create_project(db=db, project=project, owner_id=owner.id)


@router.get("/", response_model=List[schemas.Project])
def get_projects(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(connection.get_db)
):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/by_id/{project_id}", response_model=schemas.ProjectWithScans)
def get_project_by_id(
        project_id: int,
        db: Session = Depends(connection.get_db)
):
    db_project = crud.get_project_by_id(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.get("/by_name/{project_name}", response_model=schemas.ProjectWithScans)
def get_project_by_name(
        project_name: str,
        db: Session = Depends(connection.get_db)
):
    db_project = crud.get_project_by_name(db, project_name=project_name)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
