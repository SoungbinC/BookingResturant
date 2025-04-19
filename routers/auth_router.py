from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dependencies.database import get_db
from models import User, UserRole
from dependencies.config import Config
from jose import jwt
from datetime import timedelta, datetime
from dependencies.auth import require_role
from schemas.user_schema import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

# Initialize password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = Config()


# Helper function to create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    # Set the expiration time using the current time plus expires_delta or default 15 minutes
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )

    # Add expiration to the payload
    to_encode.update({"exp": expire})

    # Encode the JWT token with the payload and the secret key
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return encoded_jwt


# User registration route
@router.post("/register")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):

    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and store the new user in the database
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=(
            UserRole(user_data.role) if user_data.role else UserRole.CUSTOMER
        ),  # Default to 'CUSTOMER' role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


# User login route
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Find the user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
