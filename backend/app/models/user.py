from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, index=True)
    first_name: str = Field(nullable=False, index=True)
    last_name: str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)


class UserCreate(SQLModel):
    email: str
    first_name: str
    last_name: str
    password: str

class UserRead(SQLModel):
    id: int
    email: str
    first_name: str
    last_name: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

