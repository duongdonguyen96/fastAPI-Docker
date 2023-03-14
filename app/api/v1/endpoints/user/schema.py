# from typing import Optional
#
# from pydantic import Field
#
# from app.api.base.schema import BaseSchema, CreatedUpdatedBaseModel
#
#
# class UserInfoResponse(BaseSchema):
#     user_id: str = Field(..., description='Id người dùng')
#     username: str = Field(..., description='Tên đăng nhập')
#     full_name_vn: str = Field(..., description='Họ và tên người dùng')
#     avatar_url: Optional[str] = Field(..., description='Link avatar')
#     email: Optional[str] = Field(None, description='Email')
#
#
# class AuthResponse(BaseSchema):
#     token: str = Field(..., description='Token dùng cho các API khác')
#     user_info: UserInfoResponse = Field(..., description='Thông tin người dùng')
#
#
# EXAMPLE_RES_FAIL_LOGIN = {
#     "ex1": {
#         "summary": "Không gửi đúng basic auth",
#         "value": {
#             "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
#             "errors": [
#                 {
#                     "loc": "null",
#                     "msg": "null",
#                     "detail": "Not authenticated"
#                 }
#             ]
#         }
#     },
#     "ex2": {
#         "summary": "Sai tên đăng nhập hoặc mật khẩu",
#         "value": {
#             "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
#             "errors": [
#                 {
#                     "loc": "username, password",
#                     "msg": "USERNAME_OR_PASSWORD_INVALID",
#                     "detail": "Username or password is invalid"
#                 }
#             ]
#         }
#     }
# }
#
# EXAMPLE_RES_SUCCESS_DETAIL_USER = {
#     "ex1": {
#         "summary": "Lấy thông tin thành công",
#         "value": {
#             "data": {
#                 "user_id": "9651cdfd9a9a4eb691f9a3a125ac46b0",
#                 "username": "dev1",
#                 "full_name_vn": "Developer 1",
#                 "avatar_url": "cdn/users/avatar/dev1.jpg"
#             },
#             "errors": []
#         }
#     }
# }
#
#
# ########################################################################################################################
# # update user
# ########################################################################################################################
# class UserUpdateRequest(BaseSchema):
#     full_name_vn: str = Field(..., description='Họ và tên người dùng')
#     avatar_url: str = Field(..., description='Link avatar')
#
#
# class UserUpdateResponse(CreatedUpdatedBaseModel):
#     user_id: str = Field(..., description='Id người dùng')
#     full_name_vn: str = Field(..., description='Họ và tên người dùng')
#
#
# EXAMPLE_REQ_UPDATE_USER = {
#     "ex1": {
#         "summary": "A normal example",
#         "description": "A **normal** item works correctly.",
#         "value": {
#             "full_name_vn": "Foo",
#             "avatar_url": "/cdn/abc.jpg"
#         },
#     },
#     "ex2": {
#         "summary": "An example with converted data",
#         "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#         "value": {
#             "full_name_vn": "Foo",
#             "avatar_url": "A very nice Item"
#         },
#     }
# }
#
# EXAMPLE_RES_SUCCESS_UPDATE_USER = {
#     "ex1": {
#         "summary": "Thành công 1",
#         "value": {
#             "data": {
#                 "created_at": "16 10:46:08-10-2021",
#                 "created_by": "system",
#                 "updated_at": "16 10:46:08-10-2021",
#                 "updated_by": "system",
#                 "user_id": "9651cdfd9a9a4eb691f9a3a125ac46b0",
#                 "full_name_vn": "abc"
#             },
#             "errors": []
#         }
#     },
#     "ex2": {
#         "summary": "Thành công 2",
#         "value": {
#             "data": {
#                 "created_at": "16 10:46:50-10-2021",
#                 "created_by": "system",
#                 "updated_at": "16 10:46:50-10-2021",
#                 "updated_by": "system",
#                 "user_id": "9651cdfd9a9a4eb691f9a3a125ac46b0",
#                 "full_name_vn": "xyz"
#             },
#             "errors": []
#         }
#     }
# }
#
# EXAMPLE_RES_FAIL_UPDATE_USER = {
#     "ex1": {
#         "summary": "Không gửi đúng basic auth",
#         "value": {
#             "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
#             "errors": [
#                 {
#                     "loc": "null",
#                     "msg": "null",
#                     "detail": "Not authenticated"
#                 }
#             ]
#         }
#     },
#     "ex2": {
#         "summary": "Truyền không đúng kiểu dữ liệu",
#         "value": {
#             "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
#             "errors": [
#                 {
#                     "loc": "body -> avatar_url",
#                     "msg": "VALIDATE_ERROR",
#                     "detail": "str type expected"
#                 }
#             ]
#         }
#     }
# }
#
# ########################################################################################################################
