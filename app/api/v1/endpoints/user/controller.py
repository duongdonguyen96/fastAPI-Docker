# from fastapi.security import HTTPBasicCredentials
#
# from app.api.base.controller import BaseController
# from app.api.v1.endpoints.user.repository import (
#     repos_get_list_user, repos_get_user_info, repos_login
# )
# from app.api.v1.endpoints.user.schema import UserUpdateRequest
# from app.utils.functions import now
#
#
# class CtrUser(BaseController):
#     async def ctr_get_list_user(self):
#         users = self.call_repos(await repos_get_list_user())
#         return self.response_paging(data=users, current_page=1, total_page=1, total_item=len(users))
#
#     async def ctr_login(self, credentials: HTTPBasicCredentials):
#         auth_res = self.call_repos(await repos_login(username=credentials.username, password=credentials.password))
#
#         return self.response(data=auth_res)
#
#     async def ctr_get_current_user_info(self):
#         return self.response(data=self.current_user)
#
#     async def ctr_get_user_info(self, user_id: str):
#         info_user_data = self.call_repos(await repos_get_user_info(user_id))
#
#         return self.response(data=info_user_data)
#
#     async def ctr_update_user_info(self, user_id: str, user_update_req: UserUpdateRequest):
#         return self.response(data={
#             'user_id': user_id,
#             'full_name_vn': user_update_req.full_name_vn,
#             'created_at': now(),
#             'created_by': 'system',
#             'updated_at': now(),
#             'updated_by': 'system'
#         })
