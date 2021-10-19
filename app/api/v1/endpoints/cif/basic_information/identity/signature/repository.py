from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_signature_data(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')
    return ReposReturn(data={
        "customer_signatures": [
            {
                "date": "12/06/2021",
                "identity_image_transaction_1": "http://example.com/abc.png",
                "identity_image_transaction_2": "http://example.com/abc.png",
                "checked_flag": True
            },
            {
                "date": "30/05/2021",
                "identity_image_transaction_1": "http://example.com/abc.png",
                "identity_image_transaction_2": "http://example.com/abc.png",
                "checked_flag": False
            }
        ],
        "compare_signature": {
            "compare_image_url": "http://example.com/abc.png",
            "similar_percent": 94
        }
    })