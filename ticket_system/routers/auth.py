from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserRegister, UserLogin, TokenResponse, UserOut
#from ..services.auth_service import register_user, login_user
from ..services.auth_service import register_user, login_user
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user (role defaults to 'user')."""
    return register_user(data, db)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login and receive a JWT access token."""
    return login_user(data, db)
