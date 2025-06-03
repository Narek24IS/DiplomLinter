from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel


# Базовые схемы
class UserBase(BaseModel):
    username: str


class ProjectBase(BaseModel):
    name: str
    repository_url: str


class ScanBase(BaseModel):
    branch: str


class LinterResultBase(BaseModel):
    linter_name: str
    is_success: bool
    output: Optional[str] = None
    details: Optional[Dict[str, Any]] = None



# Схемы для создания (Create)
class UserCreate(UserBase):
    token: str


class ProjectCreate(ProjectBase):
    token: str


class ScanCreate(ScanBase):
    project_id: int


class LinterResultCreate(LinterResultBase):
    pass


# Схемы для ответов (Response)
class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Ранее orm_mode = True


class Project(ProjectBase):
    project_id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class Scan(ScanBase):
    scan_id: int
    project_id: int
    status: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    total_errors: int = 0
    total_warnings: int = 0

    class Config:
        from_attributes = True


class LinterResult(LinterResultBase):
    linter_result_id: int
    scan_id: int

    class Config:
        from_attributes = True


# Схемы с отношениями
class ProjectWithScans(Project):
    scans: List[Scan]

    class Config:
        from_attributes = True


class ScanWithResults(Scan):
    linter_results: List[LinterResult]

    class Config:
        from_attributes = True


class ProjectWithOwner(Project):
    owner: User

    class Config:
        from_attributes = True


# Схемы для аналитики
class ScanStats(BaseModel):
    total_scans: int
    successful_scans: int
    failed_scans: int


class LinterStats(BaseModel):
    linter_name: str
    total_runs: int
    success_rate: float


# Схемы для обновления (Update)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    token: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    repository_url: Optional[str] = None


class ScanUpdate(BaseModel):
    status: Optional[str] = None
    total_errors: Optional[int] = None
    total_warnings: Optional[int] = None


# Схемы для фильтрации
class ScanFilter(BaseModel):
    status: Optional[str] = None
    branch: Optional[str] = None
    min_errors: Optional[int] = None
    max_errors: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
