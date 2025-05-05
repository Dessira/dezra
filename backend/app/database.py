from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to a test SQLite DB

engine = create_engine(DATABASE_URL, echo=True)

# This function creates and returns a session for the tests
def get_test_session():
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session
