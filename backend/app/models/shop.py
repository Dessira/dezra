from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime, date, timezone
from pydantic import field_validator, model_validator
from typing import List, Optional

from app.models.item import Item

class Shop(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True)
    description: str | None = Field(default=None)
    image: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), nullable=False)
    password: str = Field(default=None, nullable=False)
    address: str = Field(default=None)
    state: str = Field(default=None)
    city: str = Field(default=None)
    country: str = Field(default=None)

class ShopLogin(SQLModel):
    email: str
    password: str
class ShopCreate(SQLModel):
    name: str
    email: str
    description: Optional[str]
    image: Optional[str]
    address: Optional[str]
    state: Optional[str]
    city: Optional[str]
    country: Optional[str]
    password: str
class ShopRead(SQLModel):
    id: int
    name: str
    email: str
    description: Optional[str]
    image: Optional[str]
    address: Optional[str]
    state: Optional[str]
    city: Optional[str]
    country: Optional[str]
    created_at: datetime

class ShopUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None