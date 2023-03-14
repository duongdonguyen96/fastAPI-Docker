from typing import Callable, Optional, Union

from fastapi import Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials, HTTPBasic, HTTPBearer
)

from app.api.base.except_custom import ExceptionHandle
from app.api.v1.endpoints.user.repository import repos_check_token
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.utils.error_messages import ERROR_INVALID_TOKEN

bearer_token = HTTPBearer()

basic_auth = HTTPBasic()


def get_current_user_from_header(is_require_login: bool = True) -> Callable:
    return _get_authorization_header if is_require_login else _get_authorization_header_optional


async def _get_authorization_header(
        scheme_and_credentials: HTTPAuthorizationCredentials = Security(bearer_token)
) -> UserInfoResponse:
    result_check_token = await repos_check_token(token=scheme_and_credentials.credentials)
    if result_check_token.is_error:
        raise ExceptionHandle(
            errors=[{'loc': None, 'msg': ERROR_INVALID_TOKEN}],
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return UserInfoResponse(**result_check_token.data)


async def _get_authorization_header_optional(
        scheme_and_credentials: Optional[HTTPAuthorizationCredentials] = Security(HTTPBearer(auto_error=False))
) -> Union[UserInfoResponse, None]:
    if scheme_and_credentials:
        return await _get_authorization_header(
            scheme_and_credentials=scheme_and_credentials
        )
    return None
