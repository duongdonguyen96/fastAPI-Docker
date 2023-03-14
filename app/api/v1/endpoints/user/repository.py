# from app.api.base.repository import ReposReturn
# from app.utils.error_messages import (
#     ERROR_INVALID_TOKEN, USER_ID_NOT_EXIST, USERNAME_OR_PASSWORD_INVALID
# )
#
# USER_ID = "9651cdfd9a9a4eb691f9a3a125ac46b0"
# USER_TOKEN = "OTY1MWNkZmQ5YTlhNGViNjkxZjlhM2ExMjVhYzQ2YjA6N2VlN2E2ZTg1MTUzN2M2YzFmYWIwMWQzODYzMWU4YTIx"
#
# USER_INFO = {
#     "user_id": str(USER_ID),
#     "username": "dev1",
#     "full_name_vn": "Developer 1",
#     "avatar_url": "cdn/users/avatar/dev1.jpg"
# }
#
#
# async def repos_get_list_user() -> ReposReturn:
#     return ReposReturn(data=[USER_INFO])
#
#
# async def repos_login(username: str, password: str) -> ReposReturn:
#     if username == 'dev1' and password == '12345678':
#         return ReposReturn(data={
#             "token": USER_TOKEN,
#             "user_info": USER_INFO
#         })
#     else:
#         return ReposReturn(is_error=True, msg=USERNAME_OR_PASSWORD_INVALID, loc='username, password')
#
#
# async def repos_check_token(token: str) -> ReposReturn:
#     if token == USER_TOKEN:
#         return ReposReturn(data=USER_INFO)
#     else:
#         return ReposReturn(is_error=True, msg=ERROR_INVALID_TOKEN, loc='token')
#
#
# async def repos_get_user_info(user_id: str) -> ReposReturn:
#     if user_id == USER_ID:
#         return ReposReturn(data=USER_INFO)
#     else:
#         return ReposReturn(is_error=True, msg=USER_ID_NOT_EXIST, loc='user_id')
