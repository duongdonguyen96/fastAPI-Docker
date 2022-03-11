from fastapi import APIRouter

from app.api.v1.endpoints.cif import router as routers_cif
from app.api.v1.endpoints.config import router as routers_config
from app.api.v1.endpoints.customer_service import view as view_customer_service
from app.api.v1.endpoints.dashboard import router as routers_dashboard
from app.api.v1.endpoints.file import view as views_file
from app.api.v1.endpoints.user import view as views_user

router = APIRouter()

router.include_router(router=views_user.router, prefix="/users", tags=["User"])

router.include_router(router=views_file.router, prefix="/files", tags=["File"])

router.include_router(router=view_customer_service.router, prefix="/post-check", tags=["KSS"])

router.include_router(router=routers_config.router, prefix="/config", tags=["Configs"])

router.include_router(router=routers_cif.router_module, prefix="/cif")

router.include_router(router=routers_dashboard.router_module, prefix="/dashboard", tags=["Dashboard"])
