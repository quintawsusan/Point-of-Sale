from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.user import Token, UserCreate, UserRead
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return auth_service.authenticate(db, form_data.username, form_data.password)


@router.get("/me", response_model=UserRead)
def me(current_user=Depends(get_current_user)):
    return current_user
