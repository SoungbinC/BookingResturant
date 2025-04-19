# schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.CUSTOMER


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True
