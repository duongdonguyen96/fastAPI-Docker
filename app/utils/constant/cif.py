CIF_ID_TEST = '123'  # cif_id dùng tạm để test
CIF_ID_NEW_TEST = 'NEW123'  # cif_id dùng tạm để test khi tạo

IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD = 'CMND'
IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD = 'CCCD'
IDENTITY_DOCUMENT_TYPE_PASSPORT = 'HO_CHIEU'

IDENTITY_DOCUMENT_TYPE = {
    IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD: 'Chứng minh nhân dân',
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD: 'Căn cước công dân',
    IDENTITY_DOCUMENT_TYPE_PASSPORT: 'Hộ chiếu'
}

HAND_SIDE_LEFT_CODE = '1'
HAND_SIDE_RIGHT_CODE = '2'

ACTIVE_FLAG_CREATE_FINGERPRINT = 1
FRONT_FLAG_CREATE_FINGERPRINT = 0
ACTIVE_FLAG_CREATE_SIGNATURE = 1

IMAGE_TYPE_FINGERPRINT = 'VT'
IMAGE_TYPE_SIGNATURE = 'CK'

STAFF_TYPE_BUSINESS_CODE = "NV_KD"
STAFF_TYPE_REFER_INDIRECT_CODE = "NV_GT_GT"

RESIDENT_ADDRESS_CODE = "THUONG_TRU"
CONTACT_ADDRESS_CODE = "TAM_TRU"

IMAGE_TYPE_CODE_IDENTITY = "GT_DD"
IMAGE_TYPE_CODE_SUB_IDENTITY = "GT_DD_P"
IMAGE_TYPE_CODE_FINGERPRINT = "VT"
IMAGE_TYPE_CODE_SIGNATURE = "CK"

IDENTITY_IMAGE_FLAG_BACKSIDE = 0
IDENTITY_IMAGE_FLAG_FRONT_SIDE = 1

CUSTOMER_COMPLETED_FLAG = 1
CUSTOMER_UNCOMPLETED_FLAG = 0

CUSTOMER_CONTACT_TYPE_EMAIL = 'EMAIL'
CUSTOMER_CONTACT_TYPE_MOBILE = 'MOBILE'

LANGUAGE_TYPE_VN = 'VN'
LANGUAGE_TYPE_EN = 'EN'

LANGUAGE_ID_VN = "1"
LANGUAGE_ID_EN = "2"

# Dùng trong table CRM_CUST_PERSONAL_RELATIONSHIP
CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN = 0
CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP = 1
