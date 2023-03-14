from pydantic import Field
from app.api.base.schema import BaseSchema


class CreateUserRq(BaseSchema):
    full_name: str = Field(..., description='Tên đầy đủ')
    email: str = Field(..., description='Thư điện tử')
    phone: str = Field(..., description='Số điện thoại')
    user_name: str = Field(..., description='Tên tài khoản', example='ddonguyen')
    password: str = Field(..., description='Số điện thoại', example='123456')


class CreateUserRes(BaseSchema):
    id: str = Field(..., description='id_user', example='103C76ECBBC144B7B589C6808C029016')
    full_name: str = Field(..., description='Tên đầy đủ', example='Dương Đỗ Nguyên')
    email: str = Field(..., description='Thư điện tử', example='ddonguyen@cmc.com.vn')
    phone: str = Field(..., description='Số điện thoại', example='0345449875')
    user_name: str = Field(..., description='Tên tài khoản', example='ddonguyen')


class ChangePassWord(BaseSchema):
    user_name: str = Field(..., description='Tài khoản', example='ddonguyen')
    old_password: str = Field(..., description='Mật khẩu cũ', example='123456')
    new_password: str = Field(..., description='Mật khẩu mới', example='0000000')
