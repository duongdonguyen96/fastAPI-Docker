from fastapi import APIRouter

from app.api.v1.endpoints.train.customer import view as views_customer

router_module = APIRouter()

# # router của thông tin train
# router_module.include_router(router=views_cif_info.router, tags=["[CIF] Information"])
#
# # step I. Thông tin cá nhân
# router_module.include_router(router=routers_step_1.router_step, prefix="/{cif_id}/basic-information",
#                              tags=['[CIF] I. TTCN'])
#
# # router đặc biệt, do không sử dụng prefix có path param là {cif_id}
# router_module.include_router(router=views_step_i_1_a.router_special, prefix="")
#
# # step II. Thông tin khác
# router_module.include_router(router=views_other_info.router, prefix="/{cif_id}/other-information",
#                              tags=['[CIF] II. TTK'])
#
# # step III. Tài khoản thanh toán
# router_module.include_router(router=routers_payment_account.router_step, prefix="/{cif_id}/payment-account",
#                              tags=['[CIF] III. TKTT'])

# step IV. E-banking
router_module.include_router(
    router=views_customer.router, prefix="/customer", tags=["[Customer]"]
)

# # step V. Thẻ ghi nợ
# router_module.include_router(router=views_debit_card.router, prefix="/{cif_id}/debit-card",
#                              tags=['[CIF] V. Thẻ ghi nợ'])
#
# # step VI. Biểu mẫu
# router_module.include_router(router=views_form.router, prefix="/{cif_id}/form",
#                              tags=['[CIF] VI. Biểu mẫu'])
