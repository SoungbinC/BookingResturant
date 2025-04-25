from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dependencies.config import config
from dependencies.database import get_db
from models import User, UserRole

from fastapi import Request
from fastapi import Cookie

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Config
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES


# Token verification function
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db),
):

    print("🐞 access_token from cookie:", access_token)  # ← Add this

    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")

    token = access_token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def require_role(required_role: UserRole):
    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403, detail="Access forbidden: insufficient permissions"
            )
        return current_user

    return role_dependency
