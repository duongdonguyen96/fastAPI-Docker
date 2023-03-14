from pydantic import json
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.train.user.model import (Customer)
from app.utils.functions import now


@auto_commit
async def create_user(session: Session, user: dict) -> ReposReturn:
    try:
        session.add(Customer(**user))
        session.flush()
    except Exception as ex:
        return ReposReturn(msg=ex, is_error=True)

    return ReposReturn(data=user)


async def get_all_user(session: Session) -> ReposReturn:
    try:
        all_users = session.query(
            Customer.id,
            Customer.full_name,
            Customer.email,
            Customer.phone,
            Customer.user_name,
            Customer.department_id,
            Customer.company_id
        ).filter(
            Customer.id is not None
        )

    except Exception as ex:
        return ReposReturn(msg=ex, is_error=True)

    return ReposReturn(data=all_users)


async def change_password_user(session: Session) -> ReposReturn:
    try:
        all_users = session.execute(
            select(
                Customer.id,
                Customer.full_name,
                Customer.email,
                Customer.phone,
                Customer.user_name,
                Customer.department_id,
                Customer.company_id
            ).filter(
                Customer.id is not None
            )
        ).all()
    except Exception as ex:
        return ReposReturn(msg=ex, is_error=True)

    return ReposReturn(data=all_users)


async def _get_user_by_username(session: Session, username) -> ReposReturn:
    try:
        user = session.execute(
            select(
                Customer
            ).filter(
                Customer.user_name == username
            )
        ).scalars().first()
    except Exception as ex:
        return ReposReturn(msg=ex, is_error=True)

    return ReposReturn(data=user)
