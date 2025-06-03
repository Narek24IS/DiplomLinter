import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from ...db import crud, schemas, connection, models
from ...linting.linter_runner import run_linting

router = APIRouter(prefix="/scans", tags=["scans"])
logger = logging.getLogger(__name__)

@router.post("/{project_id}/start", response_model=schemas.Scan)
async def start_scan(
        project_id: int,
        branch: str,
        background_tasks: BackgroundTasks,
        user = Depends(crud.get_current_user),
        db: Session = Depends(connection.get_db)
):
    db_project = crud.get_project_by_id(db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if db_project.owner_id != user.user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    # Создаем запись о сканировании
    scan = schemas.ScanCreate(project_id=project_id, branch=branch if branch else "main")
    db_scan = crud.create_scan(db=db, scan=scan, project_id=project_id)

    # Запускаем линтинг в фоне
    background_tasks.add_task(run_linting, db_scan.scan_id, db_project.repository_url, db_scan.branch)

    return db_scan


@router.get("/", response_model=List[schemas.ScanWithResults])
def get_scans(
        skip: int = 0,
        limit: int = 100,
        user = Depends(crud.get_current_user),
        db: Session = Depends(connection.get_db)
):
    scans = crud.get_scans_by_user(db, user_id=user.user_id, skip=skip, limit=limit)
    return scans


@router.get("/{scan_id}", response_model=schemas.ScanWithResults)
def get_scan(
        scan_id: int,
        user = Depends(crud.get_current_user),
        db: Session = Depends(connection.get_db)
):
    db_scan = crud.get_scan(db, scan_id=scan_id)
    if db_scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    if db_scan.project.owner_id != user.user_id:
        raise HTTPException(status_code=403, detail=f"Permission denied {scan_id} {db_scan.scan_id} {db_scan.project.owner_id} != {user.user_id}")
    return db_scan


@router.get("/project/{project_id}", response_model=List[schemas.Scan])
def get_project_scans(
        project_id: int,
        skip: int = 0,
        limit: int = 100,
        user = Depends(crud.get_current_user),
        db: Session = Depends(connection.get_db)
):
    scans = crud.get_project_scans(db, user_id=user.user_id, project_id=project_id, skip=skip, limit=limit)
    return scans
