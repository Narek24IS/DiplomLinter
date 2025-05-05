import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from ...db import crud, schemas, connection
from ...linting.linter_runner import run_linting

router = APIRouter(prefix="/scans", tags=["scans"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.Scan)
def create_scan(
        scan: schemas.ScanCreate,
        db: Session = Depends(connection.get_db)
):
    db_project = crud.get_project_by_id(db, project_id=scan.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    return crud.create_scan(project_id=scan.project_id, db=db, scan=scan)


@router.post("/{project_id}/start", response_model=schemas.Scan)
async def start_scan(
        project_id: int,
        branch: str,
        background_tasks: BackgroundTasks,
        db: Session = Depends(connection.get_db)
):
    db_project = crud.get_project_by_id(db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Создаем запись о сканировании
    scan = schemas.ScanCreate(project_id=project_id, branch=branch if branch else "main")
    db_scan = crud.create_scan(db=db, scan=scan, project_id=project_id)

    # Запускаем линтинг в фоне
    background_tasks.add_task(run_linting, db_scan.id, db_project.repository_url, db_scan.branch)

    return db_scan


@router.get("/", response_model=List[schemas.ScanWithResults])
def get_scans(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(connection.get_db)
):
    scans = crud.get_scans(db, skip=skip, limit=limit)
    return scans


@router.get("/{scan_id}", response_model=schemas.ScanWithResults)
def get_scan(
        scan_id: int,
        db: Session = Depends(connection.get_db)
):
    db_scan = crud.get_scan(db, scan_id=scan_id)
    if db_scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return db_scan


@router.get("/project/{project_id}", response_model=List[schemas.Scan])
def get_project_scans(
        project_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(connection.get_db)
):
    scans = crud.get_project_scans(db, project_id=project_id, skip=skip, limit=limit)
    return scans
