from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlmodel import Session, select
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from app.models.shop import Shop
from app.models.user import User, UserLogin
from app.database import get_session
from app.core.security import create_access_token, verify_password
from pydantic import BaseModel
from app.core.config import get_settings  # replace with actual file name (e.g., config)

settings = get_settings()
router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    session: Session = Depends(get_session),
):
    password = user.password
    user = session.exec(select(User).where(user.email == user.email)).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
async def get_current_shop(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    shop = session.exec(select(Shop).where(Shop.email == email)).first()
    if not shop:
        raise HTTPException(status_code=401, detail="Shop not found")
    return shop