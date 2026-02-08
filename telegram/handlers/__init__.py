from .common import start_router, help_router, fisca_router

routers = [
    start_router,
    help_router,
    fisca_router
    ]

__all__ = ["routers"]
