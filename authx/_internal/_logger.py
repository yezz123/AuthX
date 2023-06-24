import logging
import sys
import traceback
from typing import Optional


def get_logger() -> logging.Logger:
    return log


def set_log_level(level: str) -> logging.Logger:
    log.setLevel(level)
    return log


def log_debug(msg: str, loc: Optional[str] = None, method: Optional[str] = None) -> None:
    log.debug(msg=_build_log_msg(msg=msg, loc=loc, method=method))


def log_info(msg: str, loc: Optional[str] = None, method: Optional[str] = None) -> None:
    log.info(msg=_build_log_msg(msg=msg, loc=loc, method=method))


def log_error(msg: str, loc: Optional[str] = None, method: Optional[str] = None, e: Optional[Exception] = None) -> None:
    log.error(msg=_build_log_msg(msg=msg, loc=loc, method=method))
    log.error(msg=f"{traceback.format_exc()}")
    return


def _build_log_msg(msg: str, loc: Optional[str] = None, method: Optional[str] = None) -> str:
    log_str = f"{msg}"
    if loc:
        log_str = f"[{loc}] {log_str}"

    if method:
        log_str = f"[{loc}][{method}] {log_str}"

    return log_str


logging.basicConfig()
default_factory = logging.getLogRecordFactory()
log = logging.getLogger("authx")
logging.StreamHandler(sys.stdout)
log.setLevel(logging.DEBUG)
