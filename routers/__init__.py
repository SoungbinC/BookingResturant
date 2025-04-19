from .share_routers.restaurant_router import router as restaurant_router
from .auth_router import router as auth_router
from .customer_router import router as customer_router
from .restaurant_manager_router import router as restaurant_manager_router
from .admin_router import router as admin_router
from .profile_router import router as profile_router

__all__ = [
    "restaurant_router",
    "auth_router",
    "customer_router",
    "restaurant_manager_router",
    "admin_router",
    "profile_router",
]
