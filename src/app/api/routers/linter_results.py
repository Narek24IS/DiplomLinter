from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...db import crud, schemas, connection

router = APIRouter(prefix="/linter-results", tags=["linter_results"])


@router.get("/{linter_result_id}", response_model=List[schemas.LinterResult])
def get_linter_results(
        linter_result_id: int,
        user = Depends(crud.get_current_user),
        db: Session = Depends(connection.get_db)
):
    result = crud.get_linter_results(db, linter_result_id=linter_result_id)
    return result


@router.get("/scan/{scan_id}", response_model=List[schemas.LinterResult])
def get_scan_results(
        scan_id: int,
        user = Depends(crud.get_current_user),
        db: Session = Depends(connection.get_db)
):
    results = crud.get_scan_linter_results(db, scan_id=scan_id)
    return results


@router.get("/stats/{scan_id}", response_model=List[schemas.LinterStats])
def get_scan_stats(
        scan_id: int,
        user = Depends(crud.get_current_user),
        db: Session = Depends(connection.get_db)
):
    return crud.get_scan_stats(db, scan_id=scan_id)
