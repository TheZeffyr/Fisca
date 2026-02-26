from .users import router as user_router
from .currencies import router as currency_router
from .transactions import router as transaction_router
from .categories import router as category_router
from .savings import router as saving_router

routers = [
    user_router,
    currency_router,
    transaction_router,
    category_router,
    saving_router
]


__all__ = ["routers"]
