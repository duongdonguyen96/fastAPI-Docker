# from datetime import date
# from typing import Optional
#
# from pydantic import Field
#
# from app.api.base.schema import BaseSchema
# from app.api.v1.endpoints.train.base_field import CustomField
# from app.api.v1.schemas.utils import (
#     DropdownRequest, DropdownResponse, OptionalDropdownResponse
# )
#
#
# class AddressResponse(BaseSchema):
#     province: DropdownResponse = Field(..., description="Tỉnh/Thành phố")
#     district: DropdownResponse = Field(..., description="Quận/Huyện")
#     ward: DropdownResponse = Field(..., description="Phường/Xã")
#     number_and_street: str = Field(..., description="Số nhà, tên đường")
#
#
# class OptionalAddressResponse(BaseSchema):
#     province: OptionalDropdownResponse = Field(None, description="Tỉnh/Thành phố")
#     district: OptionalDropdownResponse = Field(None, description="Quận/Huyện")
#     ward: OptionalDropdownResponse = Field(None, description="Phường/Xã")
#     number_and_street: str = Field(None, description="Số nhà, tên đường")
#
#
# class AddressRequest(BaseSchema):
#     province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
#     district: DropdownRequest = Field(..., description="Quận/Huyện")
#     ward: DropdownRequest = Field(..., description="Phường/Xã")
#     number_and_street: str = Field(..., description="Số nhà, tên đường")
#
#
# class FingerPrintResponse(BaseSchema):
#     image_url: str = Field(..., description='Ảnh bàn tay')
#     hand_side: DropdownResponse = Field(..., description='Loại bàn tay')
#     finger_type: DropdownResponse = Field(..., description='Loại ngón tay')
#
#
# class FingerPrintRequest(BaseSchema):
#     image_url: str = Field(..., description="URL hình ảnh vân tay")
#     hand_side: DropdownRequest = Field(..., description="Bàn tay")
#     finger_type: DropdownRequest = Field(..., description="Ngón tay")
#
#
# ########################################################################################################################
# # Phần này dùng chung cho Người giám hộ, Mối quan hệ với khách hàng
# ########################################################################################################################
# # I. Thông tin cơ bản
# class BasicInformationResponse(BaseSchema):
#     cif_number: str = CustomField().CIFNumberField
#     customer_relationship: DropdownResponse = Field(..., description="Mối quan hệ với khách hàng")
#     full_name_vn: str = Field(..., description="Họ và tên")
#     date_of_birth: date = Field(..., description="Ngày sinh")
#     gender: DropdownResponse = Field(..., description="Giới tính")
#     nationality: DropdownResponse = Field(..., description="Quốc tịch")
#     telephone_number: Optional[str] = Field(..., description="Số ĐT bàn", nullable=True)
#     mobile_number: Optional[str] = Field(..., description="Số ĐTDĐ", nullable=True)
#     email: Optional[str] = Field(..., description="Email", nullable=True)
#
#
# # II. Giấy tờ định danh
# class IdentityDocumentResponse(BaseSchema):
#     identity_number: str = Field(..., description="Số CMND/CCCD/Hộ chiếu")
#     issued_date: date = Field(..., description="Ngày cấp")
#     expired_date: date = Field(..., description="Ngày hết hạn")
#     place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
#
#
# # III. Thông tin địa chỉ
# class AddressInformationResponse(BaseSchema):
#     resident_address: AddressResponse = Field(..., description="Địa chỉ thường trú")
#     contact_address: AddressResponse = Field(..., description="Địa chỉ liên hệ")
#
#
# # Thông tin dùng chung cho Mối quan hệ khách hàng, Người giám hộ
# class RelationshipResponse(BaseSchema):
#     id: str = Field(..., description="ID")
#     avatar_url: Optional[str] = Field(..., description="URL avatar")
#     basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")
#     identity_document: IdentityDocumentResponse = Field(..., description="II. Giấy tờ định danh")
#     address_information: AddressInformationResponse = Field(..., description="III. Thông tin địa chỉ")
