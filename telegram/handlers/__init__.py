from .common import start_router, help_router, fisca_router
from .currency import router as currency_router
from .pagination import router as pagination_router


routers = [
    start_router,
    help_router,
    fisca_router,
    currency_router,
    pagination_router
    ]

__all__ = ["routers"]
