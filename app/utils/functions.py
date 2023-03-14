import json
import re
import uuid
from datetime import date, datetime
from typing import Callable, Dict, Union

import orjson

from app.settings.config import (
    DATE_INPUT_OUTPUT_FORMAT, DATETIME_INPUT_OUTPUT_FORMAT
)
from app.utils.constant.utils import UTF_8

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def dropdown(data) -> dict:
    return {
        'id': data.id,
        'code': data.code,
        'name': data.name,
    }


# dropdown trả về content
def special_dropdown(data) -> dict:
    return {
        'id': data.id,
        'code': data.code,
        'content': data.content,
        'type': data.type
    }


# dropdown có trả cờ active_flag
def dropdownflag(data) -> dict:
    return {
        'id': data.id,
        'code': data.code,
        'name': data.name,
        'active_flag': data.active_flag
    }


def today():
    """
    get today
    :return: date
    """
    return date.today()


def now():
    return datetime.now()


def datetime_to_string(_time: datetime, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> str:
    if _time:
        return _time.strftime(_format)
    return ''


def string_to_datetime(string: str, default=None, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def date_to_string(_date: date, default='', _format=DATE_INPUT_OUTPUT_FORMAT) -> str:
    if _date:
        return _date.strftime(_format)
    return default


def string_to_date(string: str, default=None, _format=DATE_INPUT_OUTPUT_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def date_to_datetime(date_input: date, default=None) -> datetime:
    try:
        return datetime.combine(date_input, datetime.min.time())
    except (ValueError, TypeError):
        return default


def datetime_to_date(datetime_input: datetime, default=None) -> date:
    try:
        return datetime_input.date()
    except (ValueError, TypeError):
        return default


def end_time_of_day(datetime_input: datetime, default=None) -> datetime:
    try:
        return datetime_input.replace(hour=23, minute=59, second=59)
    except (ValueError, TypeError):
        return default


def date_string_to_other_date_string_format(
        date_input: str,
        from_format: str,
        to_format: str = DATE_INPUT_OUTPUT_FORMAT,
        default=''
):
    _date = string_to_date(date_input, _format=from_format)
    if not _date:
        return default

    return date_to_string(_date, _format=to_format, default=default)


def generate_uuid() -> str:
    """
    :return: str
    """
    return uuid.uuid4().hex.upper()


def set_id_after_inserted(schema, db_model):
    """
    Cần set uuid từ model vừa insert dưới db SQL lên schema của object tương ứng với đối tượng đó để insert vào mongdb
    :param schema:
    :param db_model:
    :return:
    """
    schema.set_uuid(db_model.uuid)


def travel_dict(d: dict, process_func: Callable):
    process_func(d)
    if isinstance(d, Dict):
        for key, value in d.items():
            if type(value) is dict:
                travel_dict(value, process_func)
            elif isinstance(value, (list, set, tuple,)):
                for item in value:
                    travel_dict(item, process_func)
            else:
                process_func((key, value))
    return d


def process_generate_uuid(d):
    if isinstance(d, dict) and ("uuid" in d) and (d["uuid"] is None):
        d.update({"uuid": generate_uuid()})


# Tính tuổi theo luật VN
def calculate_age(birth_date: date, end_date: date = date.today()) -> int:
    ages = (end_date - birth_date)
    age_number = int((ages.total_seconds()) / (365.242 * 24 * 3600))
    return age_number


def is_valid_mobile_number(mobile_number: str) -> bool:
    regex = r'0([0-9]{9})$'
    found = re.match(regex, mobile_number)
    return True if found else False


def parse_file_uuid(url: str, default='') -> str:
    matches = re.findall(r'/(\w{32})', url)
    return matches[0] if matches else default


def orjson_dumps(data: Union[dict, list]) -> json:
    return orjson.dumps(data).decode(UTF_8)


def is_valid_number(casa_account_number: str):
    regex = re.search("[0-9]+", casa_account_number)
    if not regex or len(regex.group()) != len(casa_account_number):
        return False
    return True


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
