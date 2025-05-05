from sqlmodel import SQLModel, Field
from datetime import datetime, date, timezone
from pydantic import field_validator, model_validator
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, timezone
from pydantic import field_validator, model_validator
from typing import Optional


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), nullable=False)

    expiry_date: date = Field(nullable=False)

    # Foreign key to Shop
    shop_id: int = Field(foreign_key="shop.id", nullable=False)

    @model_validator(mode="after")
    def check_expiry_date(self) -> "Item":
        if self.expiry_date <= self.created_at.date():
            raise ValueError("expiry_date must be after created_at")
        return self

class ItemCreate(SQLModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    expiry_date: date  # Adjust the type as per your needs

# Pydantic model for item updating
class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    expiry_date: Optional[date] = None  # Adjust the type as per your needs

# Pydantic model for item view/response
class ItemRead(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    shop_id: int
    
    model_config = {
        "from_attributes": True
    }
