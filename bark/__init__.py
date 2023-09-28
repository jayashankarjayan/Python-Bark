from collections.abc import Mapping
import re
from typing import Any, Dict
from types import FunctionType
from logging import Logger, LogRecord

from .handler import BarkHandler
from .domain.log_object import LogObject


def bark(logger_object: Logger):
    def inner(func: Any) -> FunctionType:
        def actual_function_execution(*args: tuple[Any], **kwargs: Dict[str, Any]):
            func_return_value = func(*args, **kwargs)
            try:
                log_format = logger_object.handlers[0].formatter._fmt
            except AttributeError:
                log_format = None

            handler: BarkHandler = logger_object.handlers[0]

            for record in handler.records:
                collect_logs(record, log_format)
            return func_return_value
        return actual_function_execution
    return inner

def collect_logs(record: LogRecord, log_format: str | None = None):
    more_data = get_more_data(record.__dict__, log_format)
    log_object = LogObject(log_level=record.levelname, service_name=record.name,
                            code=record.levelno, msg=record.msg)
    if more_data:
        log_object.more_data = more_data

    print(log_object.payload)

def get_more_data(record_data: Dict[str, Any], log_format: str | None) -> Dict[str, Any]:
    more_data: Dict[str, Any] = {}
    match_to_exclude = [
        "message", "asctime"
    ]
    if log_format:
        pattern = r'%\(([^)]+)\)'
        matches: list[str] = re.findall(pattern, log_format)

        for match in matches:
            if match not in match_to_exclude:
                more_data[match] = record_data.get(match)

    return more_data

class Bark(Logger):

    def __init__(self, name: str, level: int = 0) -> None:
        super().__init__(name, level)

    def info(self, msg: object, *args: object, exc_info = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
        print("Hmm")
        return super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def debug(self, msg: object, *args: object, exc_info = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
        return super().debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def warn(self, msg: object, *args: object, exc_info = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
        return super().warn(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def warning(self, msg: object, *args: object, exc_info = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
        return super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def error(self, msg: object, *args: object, exc_info = None, stack_info: bool = False, stacklevel: int = 1, extra: Mapping[str, object] | None = None) -> None:
        return super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    
