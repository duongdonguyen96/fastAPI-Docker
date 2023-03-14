# import json
# from typing import List, Optional, Tuple
#
# from sqlalchemy import and_, func, select
# from sqlalchemy.orm import Session
#
# from app.api.base.repository import ReposReturn
# from app.third_parties.oracle.base import Base
# from app.third_parties.oracle.models.train.form.model import (
#     Booking, BookingAccount, BookingBusinessForm, BookingCustomer
# )
# from app.third_parties.oracle.models.master_data.account import (
#     AccountStructureType
# )
# from app.third_parties.oracle.models.master_data.others import (
#     Stage, StageLane, StageStatus
# )
# from app.utils.constant.train import ACTIVE_FLAG_ACTIVED
# from app.utils.error_messages import (
#     ERROR_BEGIN_STAGE_NOT_EXIST, ERROR_ID_NOT_EXIST, ERROR_INVALID_NUMBER,
#     ERROR_NEXT_RECEIVER_NOT_EXIST
# )
# from app.utils.functions import (
#     dropdown, is_valid_number, now, special_dropdown
# )
#
#
# async def repos_get_model_object_by_id_or_code(model_id: Optional[str], model_code: Optional[str], model: Base,
#                                                loc: str, session: Session) -> ReposReturn:
#     statement = None
#
#     if model_id:
#         statement = select(model).filter(model.id == model_id)
#
#     if model_code:
#         statement = select(model).filter(model.code == model_code)
#
#     if hasattr(model, 'active_flag'):
#         statement = statement.filter(model.active_flag == ACTIVE_FLAG_ACTIVED)
#
#     obj = session.execute(statement).scalar()
#     if not obj:
#         if not loc:
#             loc = f'{str(model.tablename)}_{"id" if model_id else "code"}'
#
#         return ReposReturn(
#             is_error=True,
#             msg=ERROR_ID_NOT_EXIST,
#             loc=loc
#         )
#
#     return ReposReturn(data=obj)
#
#
# async def repos_get_model_objects_by_ids(model_ids: List[str], model: Base, loc: str, session: Session) -> ReposReturn:
#     """
#     Get model objects by ids
#     Chỉ cần truyền vào list id -> hàm sẽ tự chuyển về set(model_ids)
#     :param model_ids: danh sách các id cần lấy ra model object
#     :param model: model trong DB
#     :param loc: vị trí lỗi
#     :param session: phiên làm việc với DB bên controller
#     :return:
#     """
#     model_ids = set(model_ids)
#
#     statement = select(model).filter(model.id.in_(model_ids))
#
#     if hasattr(model, 'active_flag'):
#         statement = statement.filter(model.active_flag == 1)
#
#     objs = session.execute(statement).scalars().all()
#     if len(objs) != len(model_ids):
#         return ReposReturn(
#             is_error=True,
#             msg=ERROR_ID_NOT_EXIST,
#             loc=f'{str(model.tablename)}_id' if not loc else loc
#         )
#
#     return ReposReturn(data=objs)
#
#
# async def get_optional_model_object_by_code_or_name(
#         model: Base, session: Session,
#         model_code: Optional[str] = None, model_name: Optional[str] = None
# ) -> Optional[object]:
#     statement = None
#
#     if model_code:
#         statement = select(model).filter(model.code == model_code)
#
#     if model_name:
#         statement = select(model).filter(func.lower(model.name) == func.lower(model_name))  # TODO: check it
#
#     if statement is None:
#         return None
#
#     if hasattr(model, 'active_flag'):
#         statement = statement.filter(model.active_flag == 1)
#
#     return session.execute(statement).scalar()
#
#
# async def repos_get_data_model_config(session: Session, model: Base, country_id: Optional[str] = None,
#                                       province_id: Optional[str] = None, district_id: Optional[str] = None,
#                                       region_id: Optional[str] = None, ward_id: Optional[str] = None,
#                                       level: Optional[str] = None, parent_id: Optional[str] = None,
#                                       is_special_dropdown: bool = False, type_id: Optional[str] = None):
#     list_data_engine = select(model)
#     if hasattr(model, "country_id"):
#         list_data_engine = list_data_engine.filter(model.country_id == country_id)
#
#     if hasattr(model, "region_id") and region_id:
#         list_data_engine = list_data_engine.filter(model.region_id == region_id)
#
#     if hasattr(model, "district_id") and district_id:
#         list_data_engine = list_data_engine.filter(model.district_id == district_id)
#
#     if hasattr(model, "province_id") and province_id:
#         list_data_engine = list_data_engine.filter(model.province_id == province_id)
#
#     if hasattr(model, "ward_id") and ward_id:
#         list_data_engine = list_data_engine.filter(model.ward_id == ward_id)
#
#     if hasattr(model, "level") and level:
#         list_data_engine = list_data_engine.filter(model.level == level)
#
#     if hasattr(model, "parent_id") and parent_id:
#         list_data_engine = list_data_engine.filter(model.parent_id == parent_id)
#
#     if hasattr(model, 'active_flag'):
#         list_data_engine = list_data_engine.filter(model.active_flag == 1)
#
#     if hasattr(model, 'type'):
#         list_data_engine = list_data_engine.filter(model.type == type_id)
#
#     if hasattr(model, 'order_no'):
#         list_data_engine = list_data_engine.order_by(model.order_no)
#
#     list_data = session.execute(list_data_engine).scalars().all()
#
#     if not list_data:
#         return ReposReturn(is_error=True, msg="model doesn't have data", loc='config')
#
#     # Nếu là dropdown có content và type
#     if is_special_dropdown:
#         return ReposReturn(data=[
#             special_dropdown(data) for data in list_data
#         ])
#
#     return ReposReturn(data=[
#         dropdown(data) for data in list_data
#     ])
#
#
# async def write_transaction_log_and_update_booking(log_data: json,
#                                                    session: Session,
#                                                    business_form_id: str,
#                                                    customer_id: Optional[str] = None,
#                                                    account_id: Optional[str] = None,
#                                                    ) -> Tuple[bool, Optional[dict]]:
#     if customer_id:
#         booking = session.execute(
#             select(
#                 Booking
#             )
#             .join(
#                 BookingCustomer, and_(
#                     Booking.id == BookingCustomer.booking_id,
#                     BookingCustomer.customer_id == customer_id
#                 )
#             )
#         ).scalar()
#     elif account_id:
#         booking = session.execute(
#             select(
#                 Booking
#             )
#             .join(
#                 BookingAccount, and_(
#                     Booking.id == BookingAccount.booking_id,
#                     BookingAccount.account_id == account_id
#                 )
#             )
#         ).scalar()
#     else:
#         booking = None
#
#     if not booking:
#         return False, dict(msg='Can not found booking')
#
#     booking_business_form = session.execute(
#         select(BookingBusinessForm).filter(and_(
#             BookingBusinessForm.booking_id == booking.id,
#             BookingBusinessForm.business_form_id == business_form_id
#         ))
#     ).scalar()
#
#     # Nếu chưa có thì tạo mới
#     if not booking_business_form:
#         session.add(BookingBusinessForm(**dict(
#             booking_id=booking.id,
#             business_form_id=business_form_id,
#             save_flag=True,
#             created_at=now(),
#             updated_at=now(),
#             form_data=str(log_data)
#         )))
#         response = dict(
#             created_at=now(),
#             updated_at=now()
#         )
#
#     # Nếu có thì cập nhật
#     else:
#         booking_business_form = session.execute(
#             select(
#                 BookingBusinessForm
#             ).filter(and_(
#                 BookingBusinessForm.business_form_id == business_form_id,
#                 BookingBusinessForm.booking_id == booking.id
#             ))
#         ).scalar()
#         # Cập nhật đã hoàn thành Tab này]
#         booking_business_form.form_data = str(log_data)
#         booking_business_form.update_at = now()
#         response = dict(
#             created_at=booking_business_form.created_at,
#             updated_at=now()
#         )
#         session.commit()
#
#     return True, response
#
#
# async def repos_get_acc_structure_type(acc_structure_type_id: str, level: int, loc: str, session: Session):
#     acc_structure_type = session.execute(
#         select(
#             AccountStructureType
#         ).filter(and_(
#             AccountStructureType.level == level,
#             AccountStructureType.id == acc_structure_type_id,
#             AccountStructureType.active_flag == ACTIVE_FLAG_ACTIVED
#         ))
#     ).scalar()
#     if not acc_structure_type:
#         return ReposReturn(is_error=True, msg=ERROR_ID_NOT_EXIST, loc=loc)
#
#     return ReposReturn(data=acc_structure_type)
#
#
# async def repos_get_begin_stage(business_type_id: str, session: Session):
#     begin_stage = session.execute(
#         select(
#             StageStatus,
#             Stage
#         )
#         .join(StageStatus, Stage.status_id == StageStatus.id)
#         .filter(and_(
#             Stage.parent_id.is_(None),
#             Stage.business_type_id == business_type_id
#         ))
#     ).first()
#
#     if not begin_stage:
#         return ReposReturn(
#             is_error=True,
#             msg=ERROR_BEGIN_STAGE_NOT_EXIST,
#             detail=f"business_type_id: {business_type_id}"
#         )
#
#     return ReposReturn(data=begin_stage)
#
#
# async def repos_get_next_receiver(
#         business_type_id: str,
#         stage_id: str,
#         session: Session
# ):
#     next_receiver = session.execute(
#         select(
#             Stage,
#             StageLane
#         )
#         .join(StageLane, Stage.id == StageLane.stage_id)
#         .filter(
#             Stage.parent_id == stage_id
#         )
#     ).first()
#
#     if not next_receiver:
#         return ReposReturn(
#             is_error=True,
#             msg=ERROR_NEXT_RECEIVER_NOT_EXIST,
#             detail=f"business_type_id: {business_type_id}, stage_id: {stage_id}"
#         )
#
#     return ReposReturn(data=next_receiver)
#
#
# # async def repos_get_current_stage(
# #         business_type_id: str,
# #         stage_id: str,
# #         session: Session
# # ):
# #     current_stage = session.execute(
# #         select(
# #             TransactionStage
# #         ).filter(and_(
# #             TransactionStage.business_type_id == business_type_id,
# #
# #         ))
# #     ).scalar().first()
# #
# #     if not current_stage:
# #         return ReposReturn(
# #             is_error=True,
# #             msg=ERROR_CURRENT_STAGE_NOT_EXIST,
# #             detail=f"business_type_id: {business_type_id}, stage_id: {stage_id}"
# #         )
# #
# #     return ReposReturn(data=current_stage)
#
#
# # async def repos_get_stages(
# #
# #     session: Session
# # ):
# #     stages = session.execute(
# #         select(
# #             Stage
# #         )
# #         .filter(
# #             Stage.business_type_id == business_type_id
# #         )
# #     ).all()
# #
# #     if not stages:
# #         return ReposReturn(
# #             is_error=True,
# #             msg=ERROR_STAGE_NOT_EXIST,
# #             detail=f"stage_id: {business_type_id}"
# #         )
# #
# #     return ReposReturn(data=stages)
#
#
# # async def repos_get_stage_by_business_type(
# #         business_type_id: str,
# #         stage_id: str,
# #         session: Session
# # ):
# #     stage_data = session.execute(
# #         select(
# #             StageStatus,
# #             Stage,
# #             StageLane,
# #             Lane,
# #             StageRole,
# #             StagePhase,
# #             Phase
# #         )
# #         .join(StageStatus, Stage.status_id == StageStatus.id)
# #         .join(StageLane, Stage.id == StageLane.stage_id)
# #         .join(Lane, StageLane.lane_id == Lane.id)
# #         .join(StageRole, Stage.id == StageRole.stage_id)
# #         .join(StagePhase, Stage.id == StagePhase.stage_id)
# #         .join(Phase, StagePhase.phase_id == Phase.id)
# #         .filter(and_(
# #             Stage.business_type_id == business_type_id,
# #             Stage.id == stage_id
# #         ))
# #     ).first()
# #
# #     if not stage_data:
# #         return ReposReturn(
# #             is_error=True,
# #             msg=ERROR_STAGE_NOT_EXIST,
# #             loc=f"business_type_id: {business_type_id}, stage_id: {stage_id}"
# #         )
# #
# #     return ReposReturn(data=stage_data)
#
#
# async def repos_is_valid_number(string: str, loc: str):
#     if is_valid_number(string):
#         return ReposReturn(data=None)
#
#     return ReposReturn(is_error=True, msg=ERROR_INVALID_NUMBER, loc=loc)
