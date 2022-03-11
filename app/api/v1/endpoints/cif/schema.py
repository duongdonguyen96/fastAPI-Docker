from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse


class CifInformationResponse(BaseSchema):
    self_selected_cif_flag: bool = Field(..., description='Cờ CIF thông thường/ tự chọn. '
                                                          '`False`: thông thường. '
                                                          '`True`: tự chọn')
    cif_number: Optional[str] = CustomField(description='Số CIF yêu cầu').OptionalCIFNumberField
    customer_classification: DropdownResponse = Field(..., description='Đối tượng khách hàng')
    customer_economic_profession: DropdownResponse = Field(..., description='Mã ngành KT')
    kyc_level: DropdownResponse = Field(..., description='Cấp độ KYC')


class CheckExistCIFSuccessResponse(BaseSchema):
    is_existed: bool = Field(...,
                             description="Cờ đã tồn tại hay chưa <br>`True` => tồn tại <br>`False` => chưa tồn tại")


class CheckExistCIFRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


# ################################### lịch sử hồ sơ (log)####################################3
class ProfileHistoryOfDayResponse(BaseSchema):
    user_id: str = Field(..., description="Id người dùng")
    full_name: str = Field(..., description="Tên đầy đủ của người dùng ")
    user_avatar_url: str = Field(..., description="Url ảnh đại diện của người dùng")
    id: str = Field(..., description="Id log")
    created_at: datetime = Field(..., description='Tạo mới vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
                                 example='2021-15-12 06:07:08')
    content: str = Field(..., description="Nội dung log ")


class CifProfileHistoryResponse(BaseSchema):
    created_date: str = Field(..., description="Ngày tạo")
    logs: List[ProfileHistoryOfDayResponse] = Field(..., description="Danh sách log trong 1 ngày ")


################################################################
# Thông tin khách hàng (Customer)
################################################################

class StatusResponse(DropdownResponse):
    active_flag: bool = Field(..., description="Cờ đóng mở. `False`: Đóng. `True`: Mở")


class EmployeeResponse(BaseSchema):
    id: str = Field(..., description="Mã định danh")
    full_name_vn: str = Field(..., description="Tên tiếng việt")
    avatar_url: Optional[str] = Field(..., description="Đường dẫn hình ảnh")
    user_name: str = Field(..., description="Tên")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    job_title: str = Field(..., description="Chức danh")
    department_id: str = Field(..., description="Phòng")


class CifCustomerInformationResponse(BaseSchema):
    customer_id: str = Field(..., description="Mã định danh khách hàng")
    status: StatusResponse = Field(..., description="Trạng thái")
    cif_number: Optional[str] = CustomField().OptionalCIFNumberField
    avatar_url: Optional[str] = Field(..., description="Đường dẫn hình ảnh khách hàng")
    customer_classification: DropdownResponse = Field(..., description="Hạng khách hàng")
    full_name: str = Field(..., description="Họ tên tiếng anh")
    gender: DropdownResponse = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    mobile_number: str = Field(..., description="Số điện thoại")
    identity_number: str = Field(..., description="Số giấy tờ định danh")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Ngày hết hạn")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    marital_status: DropdownResponse = Field(..., description="Tình trạng hôn nhân")
    # TODO: thông tin về loại khách hàng khi tạo CIF chưa có
    customer_type: OptionalDropdownResponse = Field(None, description="Loại khách hàng")
    # TODO: hạng tín dụng chưa có field trong customer
    credit_rating: Optional[str] = Field(..., description="Hạng tín dụng")
    address: str = Field(..., description="Địa chỉ")
    # TODO: đang nghiên cứu employees
    # total_number_of_participant: int = Field(..., description="Tổng số người tham gia")
    # employees: List[EmployeeResponse] = Field(..., description="Danh sách nhân viên")


class SOACIFInformation(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    issued_date: str = Field(None, description="Ngày cấp số CIF")
    branch_code: str = Field(None, description="Mã chi nhánh")
    customer_type: str = Field(None, description="Loại khách hàng")


class SOACustomerInformation(BaseSchema):
    full_name: Optional[str] = Field(None, description="Họ và tên không dấu")
    full_name_vn: Optional[str] = Field(None, description="Họ và tên có dấu")
    first_name: Optional[str] = Field(None, description="Họ có dấu")
    middle_name: Optional[str] = Field(None, description="Tên lót có dấu")
    last_name: Optional[str] = Field(None, description="Họ có dấu")
    date_of_birth: Optional[str] = Field(None, description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    customer_vip_type: Optional[str] = Field(None, description="Loại VIP khách hàng")
    manage_staff_id: Optional[str] = Field(None, description="Mã nhân viên quản lý")
    director_name: Optional[str] = Field(None, description="Người đại diện( khách hàng doanh nghiệp)")
    nationality_code: Optional[str] = Field(None, description="Mã quốc tịch")
    nationality: Optional[str] = Field(None, description="Quốc tịch")
    is_staff: Optional[str] = Field(None, description="Có phải nhân viên ngân hàng")
    segment_type: Optional[str] = Field(None, description="Segment khách hàng")


class SOACustomerIdentityInformation(BaseSchema):
    identity_number: Optional[str] = Field(None, description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    # place_of_issue: OptionalDropdownResponse = Field(None, description="Nơi cấp")


class SOAAddressInfo(BaseSchema):
    province: OptionalDropdownResponse = Field(None, description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(None, description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(None, description="Phường/Xã")
    name: Optional[str] = Field(None, description="Địa chỉ")


class SOACustomerAddressInfoRes(BaseSchema):
    resident_address: SOAAddressInfo = Field(None, description="Địa chỉ thường trú")
    contact_address: SOAAddressInfo = Field(None, description="Địa chỉ liên lạc")
    email: Optional[str] = Field(None, description="Email")
    mobileNum: Optional[str] = Field(None, description="Mobile Number")
    telephoneNum: Optional[str] = Field(None, description="Telephone Number")
    phoneNum: Optional[str] = Field(None, description="Phone Number")
    faxNum: Optional[str] = Field(None, description="Số fax")


class CustomerByCIFNumberResponse(BaseSchema):
    cif_information: SOACIFInformation = Field(..., description="Thông tin CIF")
    customer_information: SOACustomerInformation = Field(..., description="Thông tin khách hàng")
    # career_information: DropdownResponse = Field(..., description="Thông tin nghề nghiệp khách hàng")
    identity_information: SOACustomerIdentityInformation = Field(...,
                                                                 description="Thông tin giấy tờ định danh khách hàng")
    address_info: SOACustomerAddressInfoRes = Field(..., description="Thông tin địa chỉ khách hàng")


class CustomerByCIFNumberRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    flat_address: bool = Field(None, description="Có chuyền về dạng flat không, mặc định là `null`")
