# from typing import Optional
#
# from pydantic import Field
#
# from app.api.base.schema import BaseSchema
#
#
# class DropdownResponse(BaseSchema):
#     id: str = Field(..., min_length=1, description='`Chuỗi định danh`')
#     code: str = Field(..., min_length=1, description='`Mã`')
#     name: str = Field(..., min_length=1, description='`Tên`')
#
#
# class OptionalDropdownResponse(BaseSchema):
#     id: Optional[str] = Field(None, min_length=1, description='`Chuỗi định danh`', nullable=True)
#     code: Optional[str] = Field(None, min_length=1, description='`Mã`', nullable=True)
#     name: Optional[str] = Field(None, min_length=1, description='`Tên`', nullable=True)
#
#
# class DropdownRequest(BaseSchema):
#     id: str = Field(..., min_length=1, description='`Chuỗi định danh`')
#
#
# class OptionalDropdownRequest(BaseSchema):
#     id: Optional[str] = Field(None, min_length=1, description='`Chuỗi định danh`', nullable=True)
#
#
# ########################################################################################################################
# # Response save
# ########################################################################################################################
# class SaveSuccessResponse(BaseSchema):
#     cif_id: str = Field(..., min_length=1, description='Id CIF ảo')
