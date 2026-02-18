from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated
from . import config

POSTGRES_URL = f"postgresql://{config.settings.database_username}:{config.settings.database_password}@{config.settings.database_host}:{config.settings.database_port}/{config.settings.database_name}"

engine = create_engine(POSTGRES_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]