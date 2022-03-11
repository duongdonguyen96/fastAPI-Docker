from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.dashboard.controller import CtrDashboard
from app.api.v1.endpoints.dashboard.schema import TransactionListResponse

router = APIRouter()


@router.get(
    path="/",
    name="Transaction List",
    description="Danh sách giao dịch",
    responses=swagger_response(
        response_model=ResponseData[TransactionListResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_transaction_list(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    transaction_list_response = await CtrDashboard().ctr_get_transaction_list()

    return ResponseData[List[TransactionListResponse]](**transaction_list_response)
