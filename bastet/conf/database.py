from sqlmodel import (
    SQLModel,
    create_engine, 
    Session,
)
import settings

# import models to be created
# FIX: Should be registered automatically
from ..store.models import Book


connection_string = f'sqlite:///{str(settings.BASE_DIR)}/db.sqlite3'
connect_args = {"check_same_thread": False}

engine = create_engine(connection_string, echo=settings.DEBUG, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def creat_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    creat_db()