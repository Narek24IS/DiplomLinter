from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    token = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.now)

    projects = relationship("Project", back_populates="owner")


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint('repository_url', name='uq_repository_url'),
    )

    project_id = Column(Integer, primary_key=True)
    repository_url = Column(String(500), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    owner_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="projects")
    scans = relationship("Scan", back_populates="project")


class ScanStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Scan(Base):
    __tablename__ = "scans"
    __table_args__ = (
        Index("ix_scans_project_id", "project_id"),
        Index("ix_scans_status", "status"),
    )

    scan_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    status = Column(String(20), default=ScanStatus.PENDING, nullable=False)
    started_at = Column(DateTime, default=datetime.now)
    finished_at = Column(DateTime)
    branch = Column(String(100))
    commit_hash = Column(String(40))
    total_errors = Column(Integer, default=0)
    total_warnings = Column(Integer, default=0)

    project = relationship("Project", back_populates="scans")
    linter_results = relationship("LinterResult", back_populates="scan")


class LinterResult(Base):
    __tablename__ = "linter_results"
    __table_args__ = (
        Index("ix_linter_results_scan_id", "scan_id"),
    )

    linter_result_id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey("scans.scan_id"), nullable=False)
    linter_name = Column(String(50), nullable=False)
    is_success = Column(Boolean, nullable=False)
    output = Column(Text)
    details = Column(JSON)

    scan = relationship("Scan", back_populates="linter_results")