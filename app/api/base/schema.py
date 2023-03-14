# from typing import Any, Generic, List, TypeVar
# from uuid import UUID
#
# import orjson
# from pydantic import BaseModel, Field
# from pydantic.generics import GenericModel
# from pydantic.schema import date, datetime
#
# from app.utils.functions import date_to_string, datetime_to_string
# from pydantic import BaseModel, conint
# from typing import Optional, Generic, TypeVar
#
# from sqlalchemy import asc, desc
# from sqlalchemy.orm import Query
# from pydantic.generics import GenericModel
# from contextvars import ContextVar
#
# TypeX = TypeVar("TypeX")
#
#
# def orjson_dumps(v, *, default):
#     # orjson.dumps returns bytes, to match standard json.dumps we need to decode
#     return orjson.dumps(v, default=default).decode()
#
#
# class BaseSchema(BaseModel):
#     class Config:
#         json_loads = orjson.loads
#         json_dumps = orjson_dumps
#         json_encoders = {
#             datetime: lambda dt: datetime_to_string(dt),
#             date: lambda d: date_to_string(d)
#         }
#
#     def set_uuid(self, uuid: [str, UUID]):
#         object.__setattr__(self, 'uuid', uuid)
#
#
# class BaseGenericSchema(BaseSchema, GenericModel):
#     pass
#
#
# class CreatedUpdatedBaseModel(BaseSchema):
#     created_at: datetime = Field(..., description='Tạo mới vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
#                                  example='2021-15-12 06:07:08')
#
#     created_by: str = Field(..., description='Tạo mới bởi')
#
#     updated_at: datetime = Field(..., description='Cập nhật vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
#                                  example='2021-15-12 06:07:08')
#
#     updated_by: str = Field(..., description='Cập nhật vào lúc')
#
#
# class Error(BaseSchema):
#     loc: str = Field(..., description='Vị trí lỗi')
#     msg: str = Field(..., description='Mã lỗi')
#     detail: str = Field(..., description='Mô tả chi tiết')
#
#
# class PagingResponse(BaseSchema, GenericModel, Generic[TypeX]):
#     data: List[TypeX] = Field(..., description='Danh sách item')
#     errors: List[Error] = []
#     total_item: int = Field(..., description='Tổng số item có trong hệ thống')
#     total_page: int = Field(..., description='Tổng số trang')
#     current_page: int = Field(..., description='Số thứ tự trang hiện tại')
#
#
# class PaginationRequest(BaseSchema):
#     page_size: Optional[conint(gt=0, lt=1001)] = 10
#     current_page: Optional[conint(gt=0)] = 1
#     # sort_by: Optional[str] = 'id'
#     # order: Optional[str] = 'desc'
#
#
# class ResponseData(BaseSchema, GenericModel, Generic[TypeX]):
#     data: TypeX = Field(..., description='Dữ liệu trả về khi success')
#     errors: List[Error] = []
#
#
# class ResponseError(BaseSchema):
#     data: Any = None
#     errors: List[Error] = Field(..., description='Lỗi trả về')
