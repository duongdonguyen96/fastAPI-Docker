from pydantic import Field

from app.api.base.schema import BaseSchema


class TransactionListResponse(BaseSchema):
    cif_id: str = Field(..., description="CIF ID")
    full_name_vn: str = Field(..., description="Tên khách hàng")
