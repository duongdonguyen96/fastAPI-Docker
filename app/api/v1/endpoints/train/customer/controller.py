from app.api.base.controller import BaseController
from app.api.v1.endpoints.train.customer.repository import (create_user, get_all_user, _get_user_by_username)
from app.api.v1.endpoints.train.customer.schema import (CreateUserRq)

from app.utils.functions import dropdown, generate_uuid, now, hash_password, verify_password
from app.utils import error_messages as ms


class CtrUser(BaseController):

    async def ctr_create_user(self, user: CreateUserRq):
        user_db = self.call_repos(await _get_user_by_username(session=self.oracle_session, username=user.user_name))
        if user_db:
            if user_db.user_name == user.user_name:
                return self.response_exception(
                    msg=ms.VALIDATE_ERROR,
                    detail="username đã tồn tại",
                    loc="ctr_create_user"
                )

        user = {
            'id': generate_uuid(),
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'user_name': user.user_name,
            'password': hash_password(user.password)
        }

        data = self.call_repos(await create_user(user=user, session=self.oracle_session))

        return self.response(data=data)

    async def get_all_user(self, params):
        query = self.call_repos(await get_all_user(session=self.oracle_session))

        return self.response_paging(query=query, params=params)

        # return self.response(data=all_users)

    async def change_password(self, user):
        user_db = self.call_repos(await _get_user_by_username(session=self.oracle_session, username=user.user_name))

        if not user_db:
            return self.response_exception(
                msg=ms.VALIDATE_ERROR,
                detail="username không tồn tại",
                loc="_get_user_by_username"
            )

        if not verify_password(user.old_password, user_db.password):
            return self.response_exception(
                msg=ms.VALIDATE_ERROR,
                detail="Mật khẩu sai",
                loc="change_password"
            )
        user_db.password = hash_password(user.new_password)

        self.oracle_session.commit()

        return self.response(data='Thay đổi mật khẩu thành công!!')
