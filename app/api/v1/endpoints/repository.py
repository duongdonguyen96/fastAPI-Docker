from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.base import Base
from app.utils.error_messages import ERROR_ID_NOT_EXIST


async def repos_get_model_object_by_id_or_code(model_id: Optional[str], model_code: Optional[str], model: Base,
                                               loc: str, session: Session) -> ReposReturn:
    statement = None

    if model_id:
        statement = select(model).filter(model.id == model_id)

    if model_code:
        statement = select(model).filter(model.code == model_code)

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    obj = session.execute(statement).scalar()
    if not obj:
        if not loc:
            loc = f'{str(model.tablename)}_{"id" if model_id else "code"}'

        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=loc
        )

    return ReposReturn(data=obj)