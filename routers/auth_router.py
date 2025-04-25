from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Cookie,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from dependencies.database import get_db
from dependencies.config import config
from dependencies.auth import get_current_user
from models import User, UserRole
from schemas.user_schema import UserRead, UserCreate

from fastapi import Request

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Config
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM


# Token creation
def create_access_token(data: dict, expires_minutes: int = 15):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_days: int = 7):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expires_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🟢 Login route
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    username = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        "access_token",
        f"Bearer {access_token}",
        httponly=True,
        secure=False,
        max_age=900,
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        "refresh_token",
        f"Bearer {refresh_token}",
        httponly=True,
        secure=False,
        max_age=604800,
        samesite="lax",
        path="/",
    )
    return response


# 🔁 Refresh token route
@router.post("/refresh")
def refresh_token(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        token = refresh_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(data={"sub": str(user.id)})

    response = JSONResponse(content={"message": "Token refreshed"})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_access_token}",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=15 * 60,
        path="/",
    )
    return response


# 🚪 Logout route
@router.post("/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


# 👤 Get current user
@router.get("/me", response_model=UserRead)
def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    print("🍪 Cookies:", request.cookies)  # <--- check if access_token is present
    return current_user


# 🆕 Register new user
@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=UserRole(user_data.role) if user_data.role else UserRole.CUSTOMER,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}
