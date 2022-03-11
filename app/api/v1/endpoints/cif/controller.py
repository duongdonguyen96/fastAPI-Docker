from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.repository import (
    repos_check_exist_cif, repos_customer_information, repos_get_cif_info,
    repos_get_initializing_customer, repos_profile_history,
    repos_retrieve_customer_information_by_cif_number,
    repos_validate_cif_number
)
from app.api.v1.endpoints.cif.schema import CustomerByCIFNumberRequest
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.utils.constant.cif import (
    CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE, DROPDOWN_NONE_DICT,
    SOA_GENDER_TYPE_MALE
)
from app.utils.constant.soa import SOA_DATETIME_FORMAT
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown, dropdownflag
)


class CtrCustomer(BaseController):
    async def ctr_cif_info(self, cif_id: str):
        cif_info = self.call_repos(
            await repos_get_cif_info(
                cif_id=cif_id,
                session=self.oracle_session
            ))
        return self.response(cif_info)

    async def ctr_profile_history(self, cif_id: str):
        profile_history = self.call_repos((await repos_profile_history(cif_id)))
        return self.response(profile_history)

    async def ctr_customer_information(self, cif_id: str):
        customer_information = self.call_repos(
            await repos_customer_information(cif_id=cif_id, session=self.oracle_session))
        first_row = customer_information[0]

        data_response = {
            "customer_id": first_row.Customer.id,
            "status": dropdownflag(first_row.CustomerStatus),
            "cif_number": first_row.Customer.cif_number if first_row.CustomerType else None,
            "avatar_url": first_row.Customer.avatar_url,
            "customer_classification": dropdown(first_row.CustomerClassification),
            "full_name": first_row.Customer.full_name,
            "gender": dropdown(first_row.CustomerGender),
            "email": first_row.Customer.email,
            "mobile_number": first_row.Customer.mobile_number,
            "identity_number": first_row.CustomerIdentity.identity_num,
            "place_of_issue": dropdown(first_row.PlaceOfIssue),
            "issued_date": first_row.CustomerIdentity.issued_date,
            "expired_date": first_row.CustomerIdentity.expired_date,
            "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
            "nationality": dropdown(first_row.AddressCountry),
            "marital_status": dropdown(first_row.MaritalStatus),
            "customer_type": dropdown(first_row.CustomerType) if first_row.CustomerType else DROPDOWN_NONE_DICT,
            "credit_rating": None,
            "address": first_row.CustomerAddress.address
        }

        return self.response(data=data_response)

    async def ctr_check_exist_cif(self, cif_number: str):
        # validate cif_number
        self.call_repos(await repos_validate_cif_number(cif_number=cif_number))

        check_exist_info = self.call_repos(
            await repos_check_exist_cif(cif_number=cif_number)
        )
        return self.response(data=check_exist_info)

    async def ctr_retrieve_customer_information_by_cif_number(
            self,
            cif_id: str,
            request: CustomerByCIFNumberRequest
    ):
        # flat_address = request.flat_address
        cif_number = request.cif_number

        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # check cif number is valid
        self.call_repos(await repos_validate_cif_number(cif_number=cif_number))

        customer_information = self.call_repos(await repos_retrieve_customer_information_by_cif_number(
            cif_number=cif_number
        ))

        cif_info = customer_information["retrieveCustomerRefDataMgmt_out"]["CIFInfo"]
        customer_info = customer_information["retrieveCustomerRefDataMgmt_out"]["customerInfo"]
        # customer_address = customer_info["address"]
        customer_identity = customer_info["IDInfo"]

        # if flat_address:
        #     resident_address_response = customer_address["address_vn"]
        #     contact_address_response = customer_address["address1"]
        # else:
        #     _, resident_address = matching_place_residence(customer_address["address_vn"])
        #     resident_address_response = {
        #         "province": resident_address["province_code"],
        #         "district": resident_address["district_code"],
        #         "ward": resident_address["ward_code"],
        #         "number_and_street": resident_address["street_name"]
        #     }
        #
        #     _, contact_address = matching_place_residence(customer_address["address1"])
        #     contact_address_response = {
        #         "province": contact_address["province_code"],
        #         "district": contact_address["district_code"],
        #         "ward": contact_address["ward_code"],
        #         "number_and_street": contact_address["street_name"]
        #     }
        cif_number = cif_info['CIFNum']
        issued_date = cif_info['CIFIssuedDate']
        branch_code = cif_info['branchCode']
        customer_type = cif_info['customerType']

        full_name = customer_info['fullname']
        full_name_vn = customer_info['fullname_vn']
        date_of_birth = customer_info['birthDay']
        customer_vip_type = customer_info['customerVIPType']
        manage_staff_id = customer_info['manageStaffID']
        director_name = customer_info['directorName']
        nationality = customer_info['nationlity']
        is_staff = customer_info['isStaff']
        segment_type = customer_info['segmentType']

        identity_number = customer_identity['IDNum']
        identity_issued_date = customer_identity['IDIssuedDate']
        identity_place_of_issue = customer_identity['IDIssuedLocation']

        gender_id = CRM_GENDER_TYPE_MALE if customer_info['gender'] == SOA_GENDER_TYPE_MALE else CRM_GENDER_TYPE_FEMALE
        gender = await self.get_model_object_by_id(
            model_id=gender_id,
            model=CustomerGender,
            loc=f"gender_id: {gender_id}"
        )

        customer_information.update({
            "cif_information": {
                "cif_number": cif_number if cif_number else None,
                "issued_date": issued_date if issued_date else None,
                "branch_code": branch_code if branch_code else None,
                "customer_type": customer_type if customer_type else None,
            },
            "customer_information": {
                "full_name": full_name if full_name else None,
                "full_name_vn": full_name_vn if full_name_vn else None,
                "date_of_birth": date_of_birth if date_of_birth else None,
                "gender": dropdown(gender),
                "customer_vip_type": customer_vip_type if customer_vip_type else None,
                "manage_staff_id": manage_staff_id if manage_staff_id else None,
                "director_name": director_name if director_name else None,
                "nationality": nationality if nationality else None,
                "is_staff": is_staff if is_staff else None,
                "segment_type": segment_type if segment_type else None,
            },
            # "career_information": career_information,
            "identity_information": {
                "identity_number": identity_number if identity_number else None,
                "issued_date": date_string_to_other_date_string_format(
                    identity_issued_date,
                    from_format=SOA_DATETIME_FORMAT
                ) if identity_issued_date else None,
                "place_of_issue": identity_place_of_issue if identity_place_of_issue else None,
            }
        })

        return self.response(data=customer_information)
