# from fastapi import APIRouter, Body, Depends
# from fastapi.security import HTTPBasicCredentials
# from starlette import status
#
# from app.api.base.schema import PagingResponse, ResponseData
# from app.api.base.swagger import swagger_response
# from app.api.v1.dependencies.authenticate import (
#     basic_auth, get_current_user_from_header
# )
# from app.api.v1.dependencies.paging import PaginationParams
# from app.api.v1.endpoints.user.controller import CtrUser
# from app.api.v1.endpoints.user.schema import (
#     EXAMPLE_REQ_UPDATE_USER, EXAMPLE_RES_FAIL_LOGIN,
#     EXAMPLE_RES_FAIL_UPDATE_USER, EXAMPLE_RES_SUCCESS_DETAIL_USER,
#     EXAMPLE_RES_SUCCESS_UPDATE_USER, AuthResponse, UserInfoResponse,
#     UserUpdateRequest, UserUpdateResponse
# )
#
# router = APIRouter()
#
#
# @router.get(
#     path="/",
#     name="List user",
#     description="Danh sách các người dùng",
#     responses=swagger_response(
#         response_model=PagingResponse[UserInfoResponse],
#         success_status_code=status.HTTP_200_OK
#     )
# )
# async def view_list_user(
#         # current_user=Depends(get_current_user_from_header()),  # noqa
#         pagination_params: PaginationParams = Depends()
# ):
#     paging_users = await CtrUser(is_init_oracle_session=False, pagination_params=pagination_params).ctr_get_list_user()
#     return PagingResponse[UserInfoResponse](**paging_users)
#
#
# @router.post(
#     path="/login/",
#     name="Login",
#     description="Đăng nhập",
#     responses=swagger_response(
#         response_model=ResponseData[AuthResponse],
#         success_status_code=status.HTTP_200_OK,
#         fail_examples=EXAMPLE_RES_FAIL_LOGIN
#     ),
# )
# async def view_login(credentials: HTTPBasicCredentials = Depends(basic_auth)):
#     data = await CtrUser(is_init_oracle_session=False).ctr_login(credentials)
#     return ResponseData[AuthResponse](**data)
#
#
# @router.get(
#     path="/me/",
#     name="Detail current user",
#     description="Lấy thông tin user hiện tại",
#     responses=swagger_response(
#         response_model=ResponseData[UserInfoResponse],
#         success_status_code=status.HTTP_200_OK,
#         success_examples=EXAMPLE_RES_SUCCESS_DETAIL_USER
#     )
# )
# async def view_retrieve_current_user(
#         current_user=Depends(get_current_user_from_header())
# ):
#     user_info = await CtrUser(is_init_oracle_session=False, current_user=current_user).ctr_get_current_user_info()
#     return ResponseData[UserInfoResponse](**user_info)
#
#
# @router.get(
#     path="/{user_id}/",
#     name="Detail",
#     description="Lấy thông tin user",
#     responses=swagger_response(
#         response_model=ResponseData[UserInfoResponse],
#         success_status_code=status.HTTP_200_OK,
#         success_examples=EXAMPLE_RES_SUCCESS_DETAIL_USER
#     )
# )
# async def view_retrieve_user(
#         user_id: str,
#         current_user=Depends(get_current_user_from_header())  # noqa
# ):
#     user_info = await CtrUser(is_init_oracle_session=False).ctr_get_user_info(user_id)
#     return ResponseData[UserInfoResponse](**user_info)
#
#
# @router.post(
#     path="/{user_id}/",
#     name="Update",
#     description="Cập nhật thông tin user",
#     responses=swagger_response(
#         response_model=ResponseData[UserUpdateResponse],
#         success_status_code=status.HTTP_200_OK,
#         success_examples=EXAMPLE_RES_SUCCESS_UPDATE_USER,
#         fail_examples=EXAMPLE_RES_FAIL_UPDATE_USER
#     ),
#     deprecated=True
# )
# async def view_update(
#         user_id: str,
#         user_update_req: UserUpdateRequest = Body(
#             ...,
#             examples=EXAMPLE_REQ_UPDATE_USER,
#         ),
#         current_user=Depends(get_current_user_from_header())
# ):
#     data = await CtrUser(
#         is_init_oracle_session=False,
#         current_user=current_user
#     ).ctr_update_user_info(user_id=user_id, user_update_req=user_update_req)
#
#     return ResponseData[UserUpdateResponse](**data)
