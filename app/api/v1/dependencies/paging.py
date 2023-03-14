# from fastapi.params import Query
#
#
# # https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/#shortcut
# class PaginationParams:
#     def __init__(
#             self,
#             limit: int = Query(default=50, ge=1, description="Số phần tử trong một trang"),
#             page: int = Query(default=1, ge=1, description="Trang số mấy?")
#     ):
#         self.limit = limit
#         self.page = page
#
#     @property
#     def offset(self):
#         return self.limit * (self.page - 1)
