from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.shop import Shop
from app.routers.auth import get_current_shop, get_current_user
from app.models.item import Item, ItemCreate, ItemUpdate, ItemRead  # Imported from the new schemas file
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)

# CREATE ITEM ROUTE
@router.post("/", response_model=ItemRead)
def create_item(
    item: ItemCreate, 
    session: Session = Depends(get_session), 
    current_user: dict = Depends(get_current_shop)
):
    # Check if the shop exists for current user
    shop = session.exec(select(Shop).where(Shop.id == current_user.id)).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    db_item = Item(**item.dict(), shop_id=shop.id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# VIEW ALL ITEMS WITH PAGINATION
@router.get("/all", response_model=List[ItemRead])
def get_all_items(
    skip: int = 0, 
    limit: int = 10, 
    session: Session = Depends(get_session)
):
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items

# VIEW ITEMS OF A PARTICULAR SHOP
@router.get("/shop/{shop_id}", response_model=List[ItemRead])
def get_shop_items(
    shop_id: int, 
    session: Session = Depends(get_session)
):
    items = session.exec(select(Item).where(Item.shop_id == shop_id)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this shop")
    return items

# VIEW SINGLE ITEM
@router.get("/{item_id}", response_model=ItemRead)
def get_item(
    item_id: int, 
    session: Session = Depends(get_session)
):
    item = session.exec(select(Item).where(Item.id == item_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# UPDATE ITEM ROUTE
@router.put("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int, 
    item: ItemUpdate, 
    session: Session = Depends(get_session)
):
    db_item = session.exec(select(Item).where(Item.id == item_id)).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# DELETE ITEM ROUTE
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int, 
    session: Session = Depends(get_session)
):
    db_item = session.exec(select(Item).where(Item.id == item_id)).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(db_item)
    session.commit()
    return {"detail": "Item deleted successfully"}

# SEARCH ITEMS ROUTE
@router.get("/search/", response_model=List[ItemRead])
def search_items(
    query: str, 
    session: Session = Depends(get_session)
):
    items = session.exec(select(Item).where(Item.name.contains(query))).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found matching the search query")
    return items
