from datetime import datetime
from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from . import models, schemas, connection


# Зависимость для получения пользователя
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),  # Стандартный заголовок
        db: Session = Depends(connection.get_db)
)->models.User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme, need Bearer",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Убираем "Bearer "
    user = get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


### Операции с пользователями
def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.token == token).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, token=user.token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


### Операции с проектами
def get_project_by_id(db: Session, project_id: int) -> Optional[models.Project]:
    return db.query(models.Project).filter(models.Project.project_id == project_id).first()


def get_project_by_name(db: Session, project_name: str):
    return db.query(models.Project).filter(models.Project.name == project_name).first()


def create_project(db: Session, project: schemas.ProjectCreate, owner_id: int):
    db_project = models.Project(
        repository_url=project.repository_url,
        name=project.name,
        owner_id=owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


### Операции со сканированиями
def create_scan(db: Session, scan: schemas.ScanCreate, project_id: int):
    db_scan = models.Scan(
        project_id=project_id,
        branch=scan.branch,
        status=models.ScanStatus.PENDING
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan


def update_scan_status(db: Session, scan_id: int, status: models.ScanStatus):
    db_scan = db.query(models.Scan).filter(models.Scan.scan_id == scan_id).first()
    if db_scan:
        db_scan.status = status
        if status == models.ScanStatus.COMPLETED:
            db_scan.finished_at = datetime.now()
        db.commit()
        db.refresh(db_scan)
    return db_scan


### Операции с результатами линтеров
def create_linter_result(db: Session, result: schemas.LinterResultCreate, scan_id: int):
    db_result = models.LinterResult(
        scan_id=scan_id,
        linter_name=result.linter_name,
        is_success=result.is_success,
        output=result.output,
        details=result.details
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


### Операции для получения всех записей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_projects_by_user(db: Session, user_id: int,
                         skip: int = 0, limit: int = 100):
    return (db.query(models.Project)
            .filter(models.Project.owner_id == user_id)
            .offset(skip).limit(limit).all())


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_scans_by_user(db: Session, user_id: int,
                      skip: int = 0, limit: int = 100):
    return (db.query(models.Scan)
            .join(models.Scan.project)
            .filter(models.Project.owner_id == user_id)
            .offset(skip).limit(limit).all())


def get_scans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Scan).offset(skip).limit(limit).all()


def get_project_scans(db: Session, user_id: int, project_id: int,
                      skip: int = 0, limit: int = 100):
    return (db.query(models.Scan)
            .join(models.Scan.project)
            .filter(models.Scan.project_id == project_id)
            .filter(models.Project.owner_id == user_id)
            .offset(skip).limit(limit).all())


def get_scan(db: Session, scan_id: int)->Optional[models.Scan]:
    return db.query(models.Scan).join(models.Scan.project).filter(models.Scan.scan_id == scan_id).first()


def get_linter_results_by_user(db: Session, user_id: int, linter_result_id: int):
    return (db.query(models.LinterResult)
            .join(models.LinterResult.scan)
            .join(models.Scan.project)
            .filter(models.Project.owner_id == user_id)
            .filter(models.LinterResult.linter_result_id == linter_result_id)
            .all())


def get_linter_results(db: Session, user_id: int, linter_result_id: int):
    return (db.query(models.LinterResult)
            .join(models.LinterResult.scan)
            .join(models.Scan.project)
            .filter(models.Project.owner_id == user_id)
            .filter(models.LinterResult.linter_result_id == linter_result_id)
            .all())


def get_scan_linter_results(db: Session, user_id: int, scan_id: int):
    return (db.query(models.LinterResult)
            .join(models.LinterResult.scan)
            .join(models.Scan.project)
            .filter(models.Project.owner_id == user_id)
            .filter(models.LinterResult.scan_id == scan_id)
            .all())


def get_scan_linter_results(db: Session, scan_id: int):
    return db.query(models.LinterResult).filter(models.LinterResult.scan_id == scan_id).all()


def get_scan_stats(db: Session, scan_id: int):
    scan: Optional[models.Scan] = db.query(models.Scan).filter(models.Scan.scan_id == scan_id).first()
    if not scan:
        return []
    results = db.query(models.LinterResult).filter(models.LinterResult.scan_id == scan_id).all()

    stats = []
    linters = {result.linter_name for result in results}

    for linter in linters:
        runs = (
            db.query(models.LinterResult)
            .filter(
                models.LinterResult.scan.has(project_id=scan.project_id),
                models.LinterResult.linter_name == linter
            )
            .all()
        )
        total_runs = len(runs)
        success_runs = sum(1 for r in runs if r.is_success)

        stats.append({
            "linter_name": linter,
            "total_runs": total_runs,
            "success_rate": success_runs / total_runs if total_runs > 0 else 0,
        })

    return stats
