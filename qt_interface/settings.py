import os
from dataclasses import dataclass


@dataclass
class Settings:
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    root_login: str = "root"
    root_password: str = "root"

    project_root: str = os.path.dirname(__file__)
    db_name: str = "linter"

settings = Settings()