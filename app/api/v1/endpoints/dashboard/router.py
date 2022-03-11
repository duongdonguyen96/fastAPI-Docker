from fastapi import APIRouter

from app.api.v1.endpoints.dashboard import view as views_dashboard_info

router_module = APIRouter()

# router của thông tin Dashboard
router_module.include_router(router=views_dashboard_info.router)
