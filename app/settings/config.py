import logging
import os
import pathlib
import sys
import time

from loguru import logger
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.settings.logging_config import InterceptHandler

ROOT_APP = str(pathlib.Path(__file__).parent.absolute().parent)

APPLICATION = {
    "version": "1.0.0",
    "project_name": os.getenv("PROJECT_NAME", "CRM"),
    "secret_key": os.getenv("SECRET_KEY", ""),
    "debug": bool(os.getenv("DEBUG", "") if os.getenv("DEBUG", "") in ["True", "true", "1"] else False),
    "allowed_hosts": list(os.getenv("ALLOWED_HOSTS", ["*"])),
    "ekyc_proxy": str(os.getenv("SERVICE_EKYC_PROXY", "")),
}

DATETIME_INPUT_OUTPUT_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_INPUT_OUTPUT_FORMAT = '%Y-%m-%d'

TIME_INPUT_OUTPUT_FORMAT = '%H:%M:%S'

DATE_INPUT_OUTPUT_EKYC_FORMAT = '%d/%m/%Y'

# logging configuration
LOGGING_LEVEL = logging.DEBUG if APPLICATION["debug"] else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access", "sqlalchemy.engine")  # noqa
logger.level("CUSTOM", no=15, color="<blue>", icon="@")
logger.level("SERVICE", no=200)

logging.getLogger().handlers = [InterceptHandler()]
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(
    handlers=[
        {"sink": sys.stderr, "level": LOGGING_LEVEL},
        {
            "sink": sys.stderr,
            "level": 200,
            "format": "<blue>{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}</blue>",
        },
    ]
)

if os.getenv("DEBUG", True):
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("query_start_time", []).append(time.time())
        logger.info("Start Query:")
        logger.debug(f"\n{statement}")
        logger.debug(parameters)


    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        logger.success("Query Complete!")
        logger.info(f"Total Time: {total * 1000} ms\n")
