from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.core.security import get_password_hash
from app.routers.auth import get_current_user
from fastapi import status

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    user.password = get_password_hash(user.password)
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserRead)
def read_own_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/update", response_model=UserRead)
def update_user(
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if user_update.first_name:
        current_user.first_name = user_update.first_name
    if user_update.last_name:
        current_user.last_name = user_update.last_name
    if user_update.password:
        current_user.password = get_password_hash(user_update.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


# Delete user account
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    session.delete(current_user)
    session.commit()
    return None