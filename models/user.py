# models/user.py
from sqlalchemy import Column, Integer, String, Enum
from .common import Base
import enum
from sqlalchemy.orm import relationship

# UserRole Enum for defining user roles
# This enum defines the different roles a user can have in the system.
# It includes CUSTOMER, MANAGER, and ADMIN roles.
# Each role is represented as a string value for easy storage in the database.


class UserRole(enum.Enum):
    CUSTOMER = "CUSTOMER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password = Column(
        String,
        nullable=False,
    )
    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.CUSTOMER,
    )

    # Relationship to reservations
    reservations = relationship(
        "Reservation",
        back_populates="user",
    )
    restaurants = relationship(
        "Restaurant",
        back_populates="owner",
    )
    reviews = relationship(
        "Review",
        back_populates="user",
    )
