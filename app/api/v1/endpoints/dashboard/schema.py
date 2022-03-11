from pydantic import Field

from app.api.base.schema import BaseSchema


class TransactionListResponse(BaseSchema):
    transaction_code: str = Field(..., description="Mã giao dịch")
    full_name_vn: str = Field(..., description="Tên khách hàng")
