from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from patterns.chain.handler_me import (
    CustomerAccessHandler,
    ManagerAccessHandler,
    AdminAccessHandler,
)
from models import User
from dependencies.database import get_db
from dependencies.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])


def get_profile_handler(user, db: Session):
    customer_handler = CustomerAccessHandler()
    manager_handler = ManagerAccessHandler()
    admin_handler = AdminAccessHandler()

    # Chain the handlers together
    customer_handler.set_next(manager_handler).set_next(admin_handler)

    # Return the response from the handler that can handle the request
    return customer_handler.handle(user, db)


@router.get("/me")
def read_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    profile_data = get_profile_handler(user, db)
    return profile_data
