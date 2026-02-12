from .users import router as user_router
from .currencies import router as currency_router


routers = [user_router, currency_router]
__all__ = ["routers"]
