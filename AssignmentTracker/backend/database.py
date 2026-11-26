import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create all tables that don't exist yet."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Give each request its own database session, then close it."""
    with Session(engine) as session:
        yield session
    