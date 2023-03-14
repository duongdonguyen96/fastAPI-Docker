# import uvicorn
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import HTTPException, RequestValidationError
# from fastapi.openapi import utils
# from fastapi.responses import ORJSONResponse
# from starlette.middleware.cors import CORSMiddleware
# from starlette.responses import JSONResponse
#
# # load file config
# load_dotenv('.env')  # noqa
#
# from app.api.base.except_custom import ExceptionHandle
# from app.api.v1.endpoints import router as v1_router
# from app.settings.config import APPLICATION
# # from app.settings.event import (
# #     create_start_app_handler, create_stop_app_handler
# # )
# from app.settings.middleware import middleware_setting
# from app.utils.error_messages import VALIDATE_ERROR
#
# app = FastAPI(
#     title=APPLICATION["project_name"],
#     debug=APPLICATION["debug"],
#     version=APPLICATION["version"],
#     docs_url="/",
#     default_response_class=ORJSONResponse,
#     openapi_url="/openapi.json" if APPLICATION["debug"] else None
# )
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=APPLICATION["allowed_hosts"] or ["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["POST", "GET"],
# )
#
# # app.add_event_handler("startup", create_start_app_handler(app))
# # app.add_event_handler("shutdown", create_stop_app_handler(app))
#
#
# app.include_router(router=v1_router.router, prefix="/api/v1")
#
#
# @app.middleware("http")
# async def time_header(request: Request, call_next):
#     return await middleware_setting(request=request, call_next=call_next)
#
#
# # handler exception
# @app.exception_handler(ExceptionHandle)
# async def except_custom(_: Request, exc: ExceptionHandle) -> JSONResponse:
#     return JSONResponse(
#         content=jsonable_encoder(
#             {"data": exc.data, "errors": exc.get_message_detail()}
#         ),
#         status_code=exc.status_code,
#     )
#
#
# # handler exception
# @app.exception_handler(RequestValidationError)
# async def request_validation_except_custom(_: Request, exc: RequestValidationError) -> JSONResponse:
#     errors = []
#     if exc.errors():
#         for temp in exc.errors():
#             errors.append(
#                 {
#                     "loc": " -> ".join([str(err) for err in temp["loc"]]) if len(temp["loc"]) != 0 else None,
#                     "msg": VALIDATE_ERROR,
#                     "detail": f"{temp['msg']}",
#                 }
#             )
#
#     return JSONResponse(
#         content=jsonable_encoder({"data": None, "errors": errors}),
#         status_code=status.HTTP_400_BAD_REQUEST,
#     )
#
#
# @app.exception_handler(HTTPException)
# async def http_except_custom(_: Request, exc: HTTPException) -> JSONResponse:
#     errors = [
#         {
#             "loc": None,
#             "msg": None,
#             "detail": f"{exc.detail}",
#         }
#     ]
#
#     return JSONResponse(
#         content=jsonable_encoder({"data": None, "errors": errors}),
#         status_code=status.HTTP_400_BAD_REQUEST,
#     )
#
# # mặc định khi generate file openapi.json có gọi hàm get_openapi_path() trong fastapi.openapi.utils
# # hàm này sẽ kiểm tra chưa có http422 thì sẽ tự thêm vào response
# # đã override lại exception validator trả về 400 nên ghi đè lại giá trị http422=400 trong utils để khỏi tạo response 422
# utils.HTTP_422_UNPROCESSABLE_ENTITY = status.HTTP_400_BAD_REQUEST
#
# if __name__ == "__main__":
#     uvicorn.run('app.main:app', host="127.0.0.1", port=9005, reload=True)
