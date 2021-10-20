from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse


# Địa chỉ trong nước giống địa chỉ (AddressResponse) chỉ thêm field Quốc gia nhưng vì None nên phải tạo lại
class DomesticAddressResponse(BaseSchema):
    country: OptionalDropdownResponse = Field(..., description="Quốc gia")
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(..., description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: Optional[str] = Field(..., description="Số nhà, tên đường")


class ForeignAddressResponse(BaseSchema):
    country: OptionalDropdownResponse = Field(..., description="Quốc gia/Khu vực")
    address_1: Optional[str] = Field(..., description="Địa chỉ 1")
    address_2: Optional[str] = Field(..., description="Địa chỉ 2")
    province: OptionalDropdownResponse = Field(..., description="Thành phố")
    state: OptionalDropdownResponse = Field(..., description="Tỉnh/Bang")
    zip_code: OptionalDropdownResponse = Field(..., description="Mã bưu chính")


class ResidentAddressContactInformationResponse(BaseSchema):
    domestic_flag: bool = Field(..., description="""Cờ địa chỉ trong nước
    \n`flag` = `True` => Địa chỉ trong nước
    \n`flag` = `False` => Địa chỉ nước ngoài""")
    domestic_address: DomesticAddressResponse = Field(..., description="Địa chỉ trong nước")
    foreign_address: ForeignAddressResponse = Field(..., description="Địa chỉ nước ngoài")


class CareerInformationContactInformationResponse(BaseSchema):
    career: DropdownResponse = Field(..., description="Nghề nghiệp")
    average_income_amount: DropdownResponse = Field(..., description="Thu nhập BQ 3 tháng gần nhất")
    company_name: str = Field(None, description="Tên cơ quan công tác")
    company_phone: str = Field(None, description="Số điện thoại cơ quan")
    company_position: DropdownResponse = Field(None, description="Chức vụ")
    company_address: str = Field(None, description="Địa chỉ cơ quan")


# Quốc gia ở địa chỉ liên lạc không bắt buộc nhập ở màn hình 01_03_03
class ContactAddressResponse(DomesticAddressResponse):
    country: DropdownResponse = Field(None, description="Quốc gia")


class ContactInformationDetailResponse(BaseSchema):
    resident_address: ResidentAddressContactInformationResponse = Field(..., description="I. Địa chỉ thường trú")
    # Địa chỉ liên lạc sẽ giống với thông tin của địa chỉ trong nước
    contact_address: ContactAddressResponse = Field(..., description="II. Địa chỉ liên lạc")
    career_information: CareerInformationContactInformationResponse = Field(..., description="III. Thông tin nghề "
                                                                                             "nghiệp")