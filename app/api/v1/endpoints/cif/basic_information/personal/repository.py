from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_personal_data(cif_id: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "basic_information": {
            "full_name_vn": "TRẦN MINH HUYỀN",
            "gender": {
                "id": "1",
                "name": "Nữ",
                "code": "Code"
            },
            "honorific": {
                "id": "1",
                "name": "Chị",
                "code": "Code"
            },
            "date_of_birth": "20/03/1995",
            "under_15_year_old_flag": False,
            "place_of_birth": {
                "id": "1",
                "name": "Hồ Chí Minh",
                "code": "Code"
            },
            "country_of_birth": {
                "id": "1",
                "name": "Việt Nam",
                "code": "Code"
            },
            "nationality": {
                "id": "1",
                "name": "Việt Nam",
                "code": "Code"
            },
            "tax_number": "DN251244124",
            "resident_status": {
                "id": "1",
                "name": "Cư trú",
                "code": "Code"
            },
            "mobile_number": "21352413652",
            "telephone_number": "0235641145",
            "email": "tranminhhuyen@gmail.com",
            "contact_method": {
                "email_flag": True,
                "mobile_number_flag": True
            },
            "marital_status": {
                "id": "1",
                "name": "Độc thân",
                "code": "12345"
            }
        }
    })