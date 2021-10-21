from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.guardian.repository import (
    repos_detail_guadian, repos_save_guadian
)
from app.api.v1.endpoints.cif.basic_information.guardian.schema import (
    SaveGuardianRequest
)


class CtrGuardian(BaseController):
    async def detail(self, cif_id: str):
        detail_guardian_info = self.call_repos(await repos_detail_guadian(cif_id=cif_id))
        return self.response(data=detail_guardian_info)

    async def save(self, cif_id, guardian_save_request: SaveGuardianRequest):
        save_guardian_info = self.call_repos(await repos_save_guadian(
            cif_id=cif_id,
            created_by=self.current_user.full_name_vn
        ))
        return self.response(data=save_guardian_info)