from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.repository import (
    repos_get_transaction_list
)


class CtrDashboard(BaseController):
    async def ctr_get_transaction_list(self):
        transaction_list = self.call_repos(await repos_get_transaction_list(
            session=self.oracle_session
        ))
        transactions = [{
            "cif_id": transaction.id,
            "full_name_vn": transaction.full_name_vn
        } for transaction in transaction_list]

        transactions = transactions[:10]

        return self.response_paging(
            data=transactions,
            total_item=len(transactions)
        )
