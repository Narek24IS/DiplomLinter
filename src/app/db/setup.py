from sqlalchemy import Connection

from .connection import engine
from .models import Base


def setup_db(app):
    @app.on_event("startup")
    def on_start():
        with engine.begin() as conn:
            # Base.metadata.drop_all(conn)  # Для тестов
            Base.metadata.create_all(conn)
