from app.api.base.controller import BaseController
from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_check_list_cif_number, repos_detail_co_owner,
    repos_get_agreement_authorizations, repos_get_casa_account,
    repos_get_customer_address, repos_get_customer_by_cif_number,
    repos_get_list_cif_number, repos_save_co_owner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)
from app.utils.constant.cif import CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
from app.utils.error_messages import (
    ERROR_CUSTOMER_IDENTITY, ERROR_CUSTOMER_IDENTITY_IMAGE,
    ERROR_CUSTOMER_INDIVIDUAL_INFO
)
from app.utils.functions import dropdown, generate_uuid


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, cif_id: str, co_owner: AccountHolderRequest):
        # lấy casa_account_id theo số cif_id
        casa_account = self.call_repos(await repos_get_casa_account(cif_id=cif_id, session=self.oracle_session))

        # lấy danh sách cif_number account request
        list_cif_number_request = []
        for cif_number in co_owner.joint_account_holders:
            list_cif_number_request.append(cif_number.cif_number)

        # check cif_number có tồn tại
        self.call_repos(
            await repos_check_list_cif_number(
                list_cif_number_request=list_cif_number_request,
                session=self.oracle_session
            )
        )
        save_account_holder = [{
            "id": generate_uuid(),
            "cif_num": cif_number.cif_number,
            "casa_account_id": casa_account,
            "joint_account_holder_flag": co_owner.joint_account_holder_flag,
            "joint_account_holder_no": 1
        } for cif_number in co_owner.joint_account_holders]

        save_account_agree = []
        for agreement in co_owner.agreement_authorization:
            for signature in agreement.signature_list:
                for account_holder in save_account_holder:
                    if signature.cif_number == account_holder['cif_num']:
                        save_account_agree.append({
                            "agreement_authorization_id": agreement.id,
                            "joint_account_holder_id": account_holder['id'],
                            "agreement_flag": agreement.agreement_flag,
                            "method_sign": agreement.method_sign
                        })

        co_owner_data = self.call_repos(
            await repos_save_co_owner(
                cif_id=cif_id,
                save_account_holder=save_account_holder,
                save_account_agree=save_account_agree,
                log_data=co_owner.json(),
                session=self.oracle_session,
                created_by=self.current_user.full_name_vn,
            )
        )

        return self.response(data=co_owner_data)

    async def ctr_co_owner(self, cif_id: str):
        account_holders, list_cif_number = await repos_get_list_cif_number(cif_id=cif_id, session=self.oracle_session)

        customers_by_list_cif = self.call_repos(
            await repos_get_customer_by_cif_number(
                list_cif_number=list_cif_number,
                session=self.oracle_session
            )
        )
        customer_address = self.call_repos(
            await repos_get_customer_address(
                list_cif_number=list_cif_number,
                session=self.oracle_session
            ))

        # lấy data address
        address_information = {}
        for row in customer_address:
            if row.CustomerAddress.customer_id not in address_information:
                address_information[row.CustomerAddress.customer_id] = {
                    "contact_address": None,
                    "resident_address": None
                }

            if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                address_information[row.CustomerAddress.customer_id]["contact_address"] = row.CustomerAddress.address

            if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                address_information[row.CustomerAddress.customer_id]["resident_address"] = row.CustomerAddress.address

        # lấy data customer
        address = None
        signature = None
        customer__signature = {}
        account__holder = {}
        for customer in customers_by_list_cif:
            if not customer.CustomerIndividualInfo:
                return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_INDIVIDUAL_INFO, loc=f'{customer.Customer.id}')

            if not customer.CustomerIdentity:
                return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_IDENTITY, loc=f'{customer.Customer.id}')
            # # gán lại giá trị cho address
            for key, values in address_information.items():
                if customer.Customer.id == key:
                    address = values

            if not customer.CustomerIdentityImage:
                return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_IDENTITY_IMAGE, loc=f'{customer.Customer.id}')
            # lấy danh sách chữ ký theo từng customer_id
            if customer.Customer.id not in customer__signature:
                customer__signature[customer.Customer.id] = []

            customer__signature[customer.Customer.id].append({
                "id": customer.CustomerIdentityImage.id,
                "image_url": customer.CustomerIdentityImage.image_url
            })
            # gán giá trị cho chứ ký
            for key, values in customer__signature.items():
                if customer.Customer.id == key:
                    signature = values

            if customer.Customer.id not in account__holder:
                account__holder[customer.Customer.id] = {
                    "id": customer.Customer.id,
                    "full_name_vn": customer.Customer.full_name_vn,
                    "basic_information": {
                        "cif_number": customer.Customer.cif_number,
                        "full_name_vn": customer.Customer.full_name_vn,
                        "customer_relationship": dropdown(customer.CustomerRelationshipType),
                        "date_of_birth": customer.CustomerIndividualInfo.date_of_birth,
                        "gender": dropdown(customer.CustomerGender),
                        "nationality": dropdown(customer.AddressCountry),
                        "mobile_number": customer.Customer.mobile_number,
                        "signature": signature
                    },
                    "identity_document": {
                        "identity_number": customer.CustomerIdentity.identity_num,
                        "identity_type": dropdown(customer.CustomerIdentityType),
                        "issued_date": customer.CustomerIdentity.issued_date,
                        "expired_date": customer.CustomerIdentity.expired_date,
                        "place_of_issue": dropdown(customer.PlaceOfIssue)
                    },
                    "address_information": address,
                }

        agreement_authorizations = self.call_repos(
            await repos_get_agreement_authorizations(session=self.oracle_session))
        agreement_authorization = [{
            "id": item.id,
            "code": item.code,
            "name": item.name,
            "active_flag": item.active_flag,
        } for item in agreement_authorizations]

        return self.response(data={
            "joint_account_holder_flag": account_holders[0].JointAccountHolder.joint_account_holder_flag,
            "number_of_joint_account_holder": len(account_holders),
            "joint_account_holders": [customer for customer in account__holder.values()],
            "agreement_authorization": agreement_authorization
        })

    async def detail_co_owner(self, cif_id: str, cif_number_need_to_find: str):
        detail_co_owner = self.call_repos(await repos_detail_co_owner(
            cif_id=cif_id,
            cif_number_need_to_find=cif_number_need_to_find,
            session=self.oracle_session
        ))

        return self.response(data=detail_co_owner)
