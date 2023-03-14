from dataclasses import dataclass
from typing import Any, List

from app.api.base.schema import Error


class BaseValidator:
    def __init__(self, session_oracle=None):
        self.session_oracle = session_oracle
        self.errors: List[Error] = []

    def append_errors(self, errors: list):
        for error in errors:
            self.errors.append(
                Error(
                    loc=" -> ".join([str(err) for err in error["loc"]]) if len(error["loc"]) != 0 else None,
                    msg=f"{error['msg']}",
                    detail=error.detail if hasattr(error, 'detail') else None
                )
            )

    def append_error(self, msg: str, loc: str = None, detail: str = ""):  # noqa
        """
        Hàm add exception để trả về
        :param msg: code exception
        :param loc: fields cần thông báo
        :param detail: Thông tin thông báo
        :return:
        """
        self.errors.append(Error(msg=msg, detail=detail, loc=loc))

    @property
    def is_success(self):
        if self.errors:
            return False
        return True


@dataclass
class ValidatorReturn:
    is_error: bool = False
    loc: str = None
    msg: str = None
    detail: str = None
    data: Any = None
