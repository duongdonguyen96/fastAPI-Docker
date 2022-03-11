from pydantic import json
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.settings.event import service_soa
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.e_banking.model import (
    EBankingInfo, EBankingInfoAuthentication,
    EBankingReceiverNotificationRelationship, EBankingRegisterBalance,
    EBankingRegisterBalanceNotification, EBankingRegisterBalanceOption,
    TdAccount
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import AccountType
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.e_banking import (
    EBankingNotification
)
from app.third_parties.oracle.models.master_data.others import (
    MethodAuthentication
)
from app.utils.constant.cif import BUSINESS_FORM_EB, CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST, ERROR_NO_DATA
from app.utils.functions import now


@auto_commit
async def repos_save_e_banking_data(
        session: Session,
        log_data: json,
        cif_id: str,
        balance_option,
        reg_balance,
        relationship,
        balance_noti,
        account_info,
        auth_method,
        created_by: str) -> ReposReturn:
    """
    1. Customer đã có E-banking => xóa dữ liệu cũ => Tạo dữ liệu mới
    2. Tạo E-banking
    """
    e_banking_info = session.execute(select(EBankingInfo).filter(EBankingInfo.customer_id == cif_id)).first()

    # 1. Xóa dữ liệu cũ
    if e_banking_info:
        session.execute(delete(EBankingInfoAuthentication).filter(
            EBankingInfoAuthentication.e_banking_info_id == e_banking_info.EBankingInfo.id))

        session.delete(e_banking_info.EBankingInfo)

        e_banking_reg_balance_id = session.execute(select(EBankingRegisterBalance.id).filter(
            EBankingRegisterBalance.customer_id == cif_id,
        )).scalars().all()

        if e_banking_reg_balance_id:
            session.execute(delete(EBankingReceiverNotificationRelationship).filter(
                EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id.in_
                (e_banking_reg_balance_id),
            ))

            session.execute(delete(EBankingRegisterBalanceNotification).filter(
                EBankingRegisterBalanceNotification.eb_reg_balance_id.in_(e_banking_reg_balance_id),
            ))

            session.execute(delete(EBankingRegisterBalanceOption).filter(
                EBankingRegisterBalanceOption.customer_id == cif_id,
            ))

            session.execute(
                delete(EBankingRegisterBalance).filter(EBankingRegisterBalance.id.in_(e_banking_reg_balance_id)))

    session.bulk_save_objects([EBankingRegisterBalanceOption(**item) for item in balance_option])
    session.bulk_save_objects([EBankingRegisterBalance(**item) for item in reg_balance])
    session.bulk_save_objects([EBankingReceiverNotificationRelationship(**item) for item in relationship])
    session.bulk_save_objects([EBankingRegisterBalanceNotification(**item) for item in balance_noti])

    session.add(EBankingInfo(**account_info))
    session.flush()

    session.bulk_save_objects([EBankingInfoAuthentication(**item) for item in auth_method])

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_EB
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_check_e_banking(cif_id: str, session: Session):
    e_banking_info = session.execute(select(EBankingInfo).filter(EBankingInfo.customer_id == cif_id)).first()
    return e_banking_info


async def repos_get_e_banking_data(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy data E-banking
    1. SMS-OTT
    2. Thông tin nhận thông báo
    3. Thông tin E-banking
    """

    # 1. SMS-OTT
    contact_types = session.execute(
        select(
            EBankingRegisterBalanceOption,
            CustomerContactType,
        ).outerjoin(
            EBankingRegisterBalanceOption,
            CustomerContactType.id == EBankingRegisterBalanceOption.customer_contact_type_id
        ).filter(
            EBankingRegisterBalanceOption.customer_id == cif_id
        )
    ).all()

    # 2. Thông tin nhận thông báo
    data_e_banking = session.execute(select(
        EBankingRegisterBalance,
        EBankingRegisterBalanceNotification,
        EBankingNotification,
        EBankingReceiverNotificationRelationship,
        CustomerRelationshipType
    ).join(
        EBankingRegisterBalanceNotification,
        EBankingRegisterBalance.id == EBankingRegisterBalanceNotification.eb_reg_balance_id
    ).outerjoin(
        EBankingReceiverNotificationRelationship,
        EBankingRegisterBalance.id == EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id
    ).outerjoin(
        CustomerRelationshipType,
        EBankingReceiverNotificationRelationship.relationship_type_id == CustomerRelationshipType.id
    ).join(
        EBankingNotification, EBankingRegisterBalanceNotification.eb_notify_id == EBankingNotification.id
    ).filter(
        EBankingRegisterBalance.customer_id == cif_id,
    )).all()

    # Thông tin E-banking
    e_bank_info = session.execute(
        select(
            EBankingInfo,
            EBankingInfoAuthentication,
            MethodAuthentication
        ).outerjoin(
            EBankingInfoAuthentication,
            MethodAuthentication.id == EBankingInfoAuthentication.method_authentication_id
        ).join(
            EBankingInfo,
            EBankingInfoAuthentication.e_banking_info_id == EBankingInfo.id
        ).filter(
            EBankingInfo.customer_id == cif_id
        )
    ).all()
    return ReposReturn(data={
        "contact_types": contact_types,
        "data_e_banking": data_e_banking,
        "e_bank_info": e_bank_info

    })


DETAIL_RESET_PASSWORD_E_BANKING_DATA = {
    "personal_customer_information": {
        "id": "1234567",
        "cif_number": "1324567",
        "customer_classification": {
            "id": "1",
            "code": "CA_NHAN",
            "name": "Cá nhân"
        },
        "avatar_url": "example.com/example.jpg",
        "full_name": "TRAN MINH HUYEN",
        "gender": {
            "id": "1",
            "code": "NU",
            "name": "Nữ"
        },
        "email": "nhuxuanlenguyen153@gmail.com",
        "mobile_number": "0896524256",
        "identity_number": "079197005869",
        "place_of_issue": {
            "id": "1",
            "code": "HCM",
            "name": "TPHCM"
        },
        "issued_date": "2021-02-18",
        "expired_date": "2021-02-18",
        "address": "144 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1, TPHCM",
        "e_banking_reset_password_method": [
            {
                "id": "1",
                "code": "SMS",
                "name": "SMS",
                "checked_flag": False
            },
            {
                "id": "2",
                "code": "EMAIL",
                "name": "EMAIL",
                "checked_flag": True
            }
        ],
        "e_banking_account_name": "huyentranminh"
    },
    "question": {
        "basic_question_1": {
            "branch_of_card": {
                "id": "123",
                "code": "MASTERCARD",
                "name": "Mastercard",
                "color": {
                    "id": "123",
                    "code": "YELLOW",
                    "name": "Vàng"
                }
            },
            "sub_card_number": 2,
            "mobile_number": "0897528556",
            "branch": {
                "id": "0897528556",
                "code": "HO",
                "name": "Hội Sở"
            },
            "method_authentication": {
                "id": "1",
                "code": "SMS",
                "name": "SMS"
            },
            "e_banking_account_name": "huyentranminh"
        },
        "basic_question_2": {
            "last_four_digits": "1234",
            "credit_limit": {
                "value": "20000000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "email": "huyentranminh126@gmail.com",
            "secret_question_or_personal_relationships": [
                {
                    "customer_relationship": {
                        "id": "1",
                        "code": "MOTHER",
                        "name": "Mẹ"
                    },
                    "mobile_number": "0867589623"
                }
            ],
            "automatic_debit_status": "",
            "transaction_method_receiver": {
                "id": "1",
                "code": "EMAIL",
                "name": "Email"
            }
        },
        "advanced_question": {
            "used_limit_of_credit_card": {
                "value": "20000000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "nearest_3d_secure": {
                "business_partner": {
                    "id": "1",
                    "code": "GRAB",
                    "name": "Grab"
                },
                "value": "125000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "one_of_two_nearest_successful_transaction": "",
            "nearest_successful_login_time": ""
        }
    },
    "document_url": "example.com/example.pdf",
    "result": {
        "confirm_current_transaction_flag": True,
        "note": "Trả lời đầy đủ các câu hỏi"
    }
}


async def repos_get_list_balance_payment_account(cif_id: str, session: Session) -> ReposReturn:
    # lấy danh sách tài khoản thanh toán theo số cif trong SOA
    customer_cif_number = session.execute(
        select(
            Customer.cif_number
        ).filter(Customer.id == cif_id)
    ).scalar()
    account_casa = None

    if customer_cif_number:
        account_casa = await service_soa.current_account_from_cif(casa_cif_number=customer_cif_number)

    return ReposReturn(data=account_casa)


async def repos_get_payment_accounts(cif_id: str, session: Session) -> ReposReturn:
    payment_accounts = session.execute(
        select(
            CasaAccount,
            AccountType
        ).join(AccountType, CasaAccount.acc_type_id == AccountType.id).filter(CasaAccount.customer_id == cif_id)
    ).all()

    if not payment_accounts:
        return ReposReturn(
            is_error=True,
            msg=ERROR_NO_DATA,
            detail="Create payment account (III. Tài khoản thanh toán) before get data",
            loc=f"cif_id: {cif_id}"
        )

    return ReposReturn(data=payment_accounts)


async def repos_get_detail_reset_password(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=DETAIL_RESET_PASSWORD_E_BANKING_DATA)


async def repos_balance_saving_account_data(cif_id: str, session: Session) -> ReposReturn:
    # cif_number_saving_account = session.execute(
    #     select(
    #         Customer.cif_number
    #     ).filter(Customer.id == cif_id)
    # ).scalar()
    # saving_account = None
    # if cif_number_saving_account:
    #     saving_account = await service_soa.deposit_account_from_cif(saving_cif_number=cif_number_saving_account)

    saving_accounts = session.execute(
        select(
            Customer,
            TdAccount
        ).filter(Customer.id == cif_id)
    ).all()

    if not saving_accounts:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    response_datas = [
        {
            "id": td_account.id,
            "account_number": td_account.td_account_number,
            "name": customer.full_name_vn,
            "checked_flag": td_account.active_flag

        } for customer, td_account in saving_accounts]

    return ReposReturn(data=response_datas)


async def repos_get_detail_reset_password_teller(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "personal_customer_information": {
            "id": "1234567",
            "cif_number": "1324567",
            "customer_classification": {
                "id": "1",
                "code": "CANHAN",
                "name": "Cá nhân"
            },
            "avatar_url": "example.com/example.jpg",
            "full_name": "TRAN MINH HUYEN",
            "gender": {
                "id": "1",
                "code": "NU",
                "name": "Nữ"
            },
            "email": "nhuxuanlenguyen153@gmail.com",
            "mobile_number": "0896524256",
            "identity_number": "079197005869",
            "place_of_issue": {
                "id": "1",
                "code": "HCM",
                "name": "TPHCM"
            },
            "issued_date": "2019-02-01",
            "expired_date": "2032-03-02",
            "address": "144 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1, TPHCM",
            "e_banking_reset_password_method": [
                {
                    "id": "1",
                    "code": "SMS",
                    "name": "SMS",
                    "checked_flag": False
                },
                {
                    "id": "2",
                    "code": "EMAIL",
                    "name": "EMAIL",
                    "checked_flag": True
                }
            ],
            "e_banking_account_name": "huyentranminh"
        },
        "document": {
            "id": "1",
            "name": "Biểu mẫu đề nghị cấp lại mật khẩu Ebanking",
            "url": "https://example.com/abc/pdf",
            "version": "1.0",
            "created_by": "Nguyễn Phúc",
            "created_at": "2020-02-01 08:40",
            "active_flag": True
        }
    })
