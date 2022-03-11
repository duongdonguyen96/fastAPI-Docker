from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.settings.service import SERVICE
from app.utils.address_functions.functions import matching_place_residence
from app.utils.constant.cif import (
    CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE, SOA_GENDER_TYPE_MALE
)
from app.utils.constant.soa import (
    SOA_CASA_REPONSE_STATUS_SUCCESS, SOA_DATETIME_FORMAT,
    SOA_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA,
    SOA_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF,
    SOA_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT,
    SOA_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF,
    SOA_REPONSE_STATUS_SUCCESS
)
from app.utils.error_messages import ERROR_INVALID_URL, MESSAGE_STATUS
from app.utils.functions import date_string_to_other_date_string_format


class ServiceSOA:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["soa"]['url']
    username = SERVICE["soa"]["authorization_username"]
    password = SERVICE["soa"]["authorization_password"]
    soa_basic_auth = aiohttp.BasicAuth(login=username, password=password, encoding='utf-8')

    def start(self):
        self.session = aiohttp.ClientSession(auth=self.soa_basic_auth)

    async def stop(self):
        await self.session.close()
        self.session = None

    async def retrieve_customer_ref_data_mgmt(self, cif_number: str, flat_address: Optional[bool] = False):
        """
        Input:
            cif_number - Số CIF
            flat_address
                - True lấy thông tin địa chỉ là string
                - False lấy thông tin địa chỉ là dict
        Output: (is_success, is_existed/error_message) - Thành công, Có tồn tại/ Lỗi Service SOA
        Trả về thông tin địa chỉ là 1 address có mã Code
        """
        is_success = True
        request_data = {
            "retrieveCustomerRefDataMgmt_in": {
                "transactionInfo": {
                    "clientCode": "INAPPTABLET",  # TODO
                    "cRefNum": "CRM1641783511239",  # TODO
                    "branchInfo": {
                        "branchCode": "001"  # TODO
                    }
                },
                "CIFInfo": {
                    "CIFNum": cif_number
                }
            }
        }
        api_url = f"{self.url}{SOA_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT}"
        return_data = dict(
            is_existed=False
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[SOA] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    logger.error(f"[STATUS]{str(response.status)} [ERROR_INFO]")
                    return_data.update(message="Service SOA Status error please try again later")
                    return False, return_data

                response_data = await response.json()

                # Nếu tồn tại CIF
                if response_data["retrieveCustomerRefDataMgmt_out"]["transactionInfo"]["transactionReturn"] == SOA_REPONSE_STATUS_SUCCESS:
                    customer_info = response_data["retrieveCustomerRefDataMgmt_out"]["customerInfo"]
                    customer_address = customer_info["address"]
                    customer_identity = customer_info["IDInfo"]

                    if flat_address:
                        resident_address_response = customer_address["address_vn"]
                        contact_address_response = customer_address["address1"]
                    else:
                        _, resident_address = matching_place_residence(customer_address["address_vn"])
                        resident_address_response = {
                            "province": resident_address["province_code"],
                            "district": resident_address["district_code"],
                            "ward": resident_address["ward_code"],
                            "number_and_street": resident_address["street_name"]
                        }

                        _, contact_address = matching_place_residence(customer_address["address1"])
                        contact_address_response = {
                            "province": contact_address["province_code"],
                            "district": contact_address["district_code"],
                            "ward": contact_address["ward_code"],
                            "number_and_street": contact_address["street_name"]
                        }

                    return_data.update({
                        "is_existed": True,
                        "data": {
                            "id": cif_number,
                            "avatar_url": None,  # TODO
                            "basic_information": {
                                "cif_number": cif_number,
                                "full_name_vn": customer_info["fullname_vn"] if customer_info["fullname_vn"] else None,
                                "date_of_birth": date_string_to_other_date_string_format(
                                    customer_info["birthDay"],
                                    from_format=DATETIME_INPUT_OUTPUT_FORMAT
                                ) if customer_info["birthDay"] else None,
                                "gender": CRM_GENDER_TYPE_MALE
                                if customer_info["gender"] == SOA_GENDER_TYPE_MALE
                                else CRM_GENDER_TYPE_FEMALE,
                                "nationality": customer_info["nationlityCode"],
                                "telephone_number": customer_address["telephoneNum"],
                                "mobile_number": customer_address["mobileNum"],
                                "email": customer_address["email"],
                            },
                            "identity_document": {
                                "identity_number": customer_identity["IDNum"],
                                "issued_date": date_string_to_other_date_string_format(
                                    customer_identity["IDIssuedDate"],
                                    from_format=SOA_DATETIME_FORMAT
                                ) if customer_identity["IDIssuedDate"] else None,
                                "place_of_issue": customer_identity["IDIssuedLocation"],
                                # TODO: T ĐỒNG THÁP/ĐỒNG THÁP
                                "expired_date": None  # TODO
                            },
                            "address_information": {
                                "contact_address": contact_address_response,
                                "resident_address": resident_address_response
                            }
                        }
                    })

        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return_data.update(message="Connect to service SOA error please try again later")
            return False, return_data

        except KeyError as ex:
            logger.error(str(ex))
            return_data.update(message="Key error " + str(ex))
            return False, return_data

        except aiohttp.InvalidURL as ex:
            logger.error(str(ex))
            return_data.update(message=MESSAGE_STATUS[ERROR_INVALID_URL] + ": " + str(ex))
            return False, return_data

        return is_success, return_data

    async def retrieve_current_account_casa(self, casa_account_number):
        """
            Input:
                casa_account_number - Số tài khoản thanh toán
            Output: (is_success, is_existed/error_message) - Thành công, Có tồn tại/ Lỗi Service SOA
        """
        request_data = {
            "retrieveCurrentAccountCASA_in": {
                "transactionInfo": {
                    "clientCode": "INAPPTABLET",  # TODO
                    "cRefNum": "CRM1641783511239",  # TODO
                    "branchInfo": {
                        "branchCode": "000"  # TODO
                    }
                },
                "accountInfo": {
                    "accountNum": casa_account_number
                }
            }
        }

        api_url = f"{self.url}{SOA_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA}"
        return_data = dict(
            is_existed=True
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[SOA] {response.status} {api_url}")

                if response.status != status.HTTP_200_OK:
                    return_data.update(message=response.status)
                    return False, return_data
                else:
                    data = await response.json()
                    return_data.update(data)
                    # Nếu KHÔNG tồn tại tài khoản thanh toán
                    if data['retrieveCurrentAccountCASA_out']['transactionInfo']['transactionErrorCode'] != SOA_CASA_REPONSE_STATUS_SUCCESS:
                        return_data.update(is_existed=False)
                    return True, return_data

        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return_data.update(message="Connect to service SOA error please try again later")
            return False, return_data

        except KeyError as ex:
            logger.error(str(ex))
            return_data.update(message="Key error " + str(ex))
            return False, return_data

        except aiohttp.InvalidURL as ex:
            logger.error(str(ex))
            return_data.update(message=MESSAGE_STATUS[ERROR_INVALID_URL] + ": " + str(ex))
            return False, return_data

    async def current_account_from_cif(self, casa_cif_number):
        request_data = {
            "selectCurrentAccountFromCIF_in": {
                "transactionInfo": {
                    "clientCode": "INAPPTABLET",
                    "cRefNum": "CRM1641783511239",
                    "branchInfo": {
                        "branchCode": "001"
                    }
                },
                "CIFInfo": {
                    "CIFNum": casa_cif_number,
                    "branchCode": ""
                },
                "accountInfo": {
                    "accountCurrency": ""
                }
            }
        }
        api_url = f"{self.url}{SOA_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF}"

        return_data = dict(
            is_existed=True
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[SOA] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    return_data.update(message=response.status)
                    return False, return_data
                else:
                    data = await response.json()
                    return_data.update(data)
                    # Nếu KHÔNG tồn tại số CIF
                    # if data['retrieveCurrentAccountCASA_out']['transactionInfo'][
                    #     'transactionErrorCode'] != SOA_CASA_REPONSE_STATUS_SUCCESS:
                    #     return_data.update(is_existed=False)
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, data

    async def deposit_account_from_cif(self, saving_cif_number):
        request_data = {
            "selectDepositAccountFromCIF_in": {
                "transactionInfo": {
                    "clientCode": "INAPPTABLET",
                    "cRefNum": "CRM1641783511239",
                    "branchInfo": {
                        "branchCode": "001"
                    }
                },
                "CIFInfo": {
                    "CIFNum": saving_cif_number
                }
            }
        }
        api_url = f"{self.url}{SOA_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF}"

        return_data = dict(
            is_existed=True
        )
        data = None
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[SOA] {response.status} {api_url}")

                if response.status != status.HTTP_200_OK:
                    return_data.update(message=response.status)
                    return False, return_data
                else:
                    data = await response.json()
                    return_data.update(data)
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return data

    ####################################################################################################################
    # Thông tin khách hàng dùng chung thông qua số CIF
    ####################################################################################################################
    async def retrieve_customer_information_by_cif_number(self, cif_number: str):
        """
        Input:
            cif_number - Số CIF
            flat_address
                - True lấy thông tin địa chỉ là string
                - False lấy thông tin địa chỉ là dict
        Output: (is_success, is_existed/error_message) - Thành công, Có tồn tại/ Lỗi Service SOA
        Trả về thông tin địa chỉ là 1 address có mã Code
        """
        is_success = True
        request_data = {
            "retrieveCustomerRefDataMgmt_in": {
                "transactionInfo": {
                    "clientCode": "INAPPTABLET",  # TODO
                    "cRefNum": "CRM1641783511239",  # TODO
                    "branchInfo": {
                        "branchCode": "001"  # TODO
                    }
                },
                "CIFInfo": {
                    "CIFNum": cif_number
                }
            }
        }
        api_url = f"{self.url}{SOA_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT}"
        return_data = dict(
            is_existed=False
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[SOA] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    logger.error(f"[STATUS]{str(response.status)} [ERROR_INFO]")
                    return_data.update(message="Service SOA Status error please try again later")
                    return False, return_data

                response_data = await response.json()

                # Nếu tồn tại CIF
                if response_data["retrieveCustomerRefDataMgmt_out"]["transactionInfo"]["transactionReturn"] == SOA_REPONSE_STATUS_SUCCESS:
                    return True, response_data

        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return_data.update(message="Connect to service SOA error please try again later")
            return False, return_data

        except KeyError as ex:
            logger.error(str(ex))
            return_data.update(message="Key error " + str(ex))
            return False, return_data

        except aiohttp.InvalidURL as ex:
            logger.error(str(ex))
            return_data.update(message=MESSAGE_STATUS[ERROR_INVALID_URL] + ": " + str(ex))
            return False, return_data

        return is_success, return_data
