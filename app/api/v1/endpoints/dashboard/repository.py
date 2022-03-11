
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)


async def repos_get_transaction_list(session: Session):

    transaction_list = session.execute(
        select(
            Customer
        )
        .order_by(desc(Customer.open_cif_at))
    ).scalars().all()

    return ReposReturn(data=transaction_list)
