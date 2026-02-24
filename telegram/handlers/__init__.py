from .common import start_router, help_router, fisca_router
from .currency import router as currency_router
from .pagination import router as pagination_router
from .transaction.add import router as transaction_add_router
from .saving.create import router as saving_create_router
from .saving.view import router as saving_view_router

routers = [
    start_router,
    help_router,
    fisca_router,
    currency_router,
    pagination_router,
    transaction_add_router,
    saving_create_router,
    saving_view_router
]

__all__ = ["routers"]
