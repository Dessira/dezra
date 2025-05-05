from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.item import Item
from app.models.shop import Shop, ShopCreate, ShopRead, ShopLogin
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import get_settings
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, exceptions as jwt_exceptions
router = APIRouter(
    prefix="/shop",
    tags=["shop"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)
settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="shop/login")


@router.post("/", response_model=ShopRead)
def register_shop(shop: ShopCreate, session: Session = Depends(get_session)):
    shop.password = get_password_hash(shop.password)
    db_shop = Shop(**shop.model_dump())
    session.add(db_shop)
    session.commit()
    session.refresh(db_shop)
    return db_shop


@router.post("/login")
def login_shop(shop: ShopLogin, session: Session = Depends(get_session)):
    db_shop = session.exec(select(Shop).where(Shop.email == shop.email)).first()
    if not db_shop or not verify_password(shop.password, db_shop.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_shop.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=ShopRead)
def get_current_shop(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except jwt_exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_shop = session.exec(select(Shop).where(Shop.email == email)).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop


@router.put("/update", response_model=ShopRead)
def update_shop(
    updated_shop: ShopCreate,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except jwt_exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_shop = session.exec(select(Shop).where(Shop.email == email)).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    for key, value in updated_shop.dict().items():
        if key == "password":
            value = get_password_hash(value)
        setattr(db_shop, key, value)

    session.add(db_shop)
    session.commit()
    session.refresh(db_shop)
    return db_shop

@router.delete("/{shop_id}", status_code=204)
def delete_shop(shop_id: int, session: Session = Depends(get_session)):
    # Get the shop
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Delete all items associated with the shop
    session.exec(select(Item).where(Item.shop_id == shop_id)).delete(synchronize_session=False)

    # Delete the shop
    session.delete(shop)
    session.commit()
    return {"message": "Shop and all associated items deleted successfully"}