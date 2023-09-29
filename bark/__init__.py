from collections.abc import Mapping
import re
from typing import Any, Dict
from types import FunctionType
from logging import Logger, LogRecord, INFO, ERROR, DEBUG, WARN, WARNING

import requests

from .exceptions import BarkHandlerNotFound, NoHandlersFound, BarkLogInsertionFailed
from .configs import config
from .handler import BarkHandler, handler_object
from .domain.log_object import LogObject


def validate_handler(logger_object: Logger):
    if not handler_object.handler:
        if not logger_object.hasHandlers():
            raise NoHandlersFound("No handlers have been added to logger instance")

        for handler in logger_object.handlers:
            if isinstance(handler, BarkHandler):
                handler_object.handler = handler
                break

        if not handler_object.handler:
            raise BarkHandlerNotFound("Handler of type BarkHandler not found")


def collect_logs(record: LogRecord, log_format: str | None = None):
    more_data = get_more_data(record.__dict__, log_format)
    log_object = LogObject(
        log_level=record.levelname,
        service_name=record.name,
        code=record.levelno,
        msg=record.msg,
    )
    if more_data:
        log_object.more_data = more_data

    return log_object.payload


def get_more_data(
    record_data: Dict[str, Any], log_format: str | None
) -> Dict[str, Any]:
    more_data: Dict[str, Any] = {}
    match_to_exclude = ["message", "asctime"]
    if log_format:
        pattern = r"%\(([^)]+)\)"
        matches: list[str] = re.findall(pattern, log_format)

        for match in matches:
            if match not in match_to_exclude:
                more_data[match] = record_data.get(match)

    return more_data


def make_bulk_bark_request(logger_object: Logger):
    try:
        log_format = logger_object.handlers[0].formatter._fmt
    except AttributeError:
        log_format = None

    request_body = []
    for record in handler_object.handler.records:
        request_body.append(collect_logs(record, log_format))

    try:
        url = f"{config.bark_url}/insertMultiple"
        response: requests.Response = requests.post(url, json=request_body)
        assert (
            response.status_code == requests.codes.ok
        ), "Failed to add logs to bark database"
    except AssertionError:
        raise BarkLogInsertionFailed(response.content)


def bark(logger_object: Logger):
    validate_handler(logger_object)

    def inner(func: Any) -> FunctionType:
        def actual_function_execution(*args: tuple[Any], **kwargs: Dict[str, Any]):
            func_return_value = func(*args, **kwargs)
            make_bulk_bark_request(logger_object)
            return func_return_value

        return actual_function_execution

    return inner


class Bark(Logger):

    def __init__(self, name: str, level: int = 0) -> None:
        super().__init__(name, level)
        self.name = name

    @classmethod
    def insert_single_bark_record(cls, payload: Dict[str, Any]):
        try:
            url = f"{config.bark_url}/insertSingle"
            response: requests.Response = requests.post(url, json=payload)
            assert (
                response.status_code == requests.codes.ok
            ), "Failed to add log to bark database"
        except AssertionError:
            raise BarkLogInsertionFailed(response.content)

    def info(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        bark_log = LogObject(
            log_level="INFO",
            more_data=extra,
            service_name=self.name, code=INFO,
            msg=msg
        )
        Bark.insert_single_bark_record(bark_log.payload)
    
        return super().info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def debug(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        bark_log = LogObject(
            log_level="DEBUG",
            more_data=extra,
            service_name=self.name, code=DEBUG,
            msg=msg
        )
        Bark.insert_single_bark_record(bark_log.payload)
        return super().debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def warn(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        bark_log = LogObject(
            log_level="WARN",
            more_data=extra,
            service_name=self.name, code=WARN,
            msg=msg
        )
        Bark.insert_single_bark_record(bark_log.payload)
        return super().warn(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def warning(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        bark_log = LogObject(
            log_level="WARNING",
            more_data=extra,
            service_name=self.name, code=WARNING,
            msg=msg
        )
        Bark.insert_single_bark_record(bark_log.payload)
        return super().warning(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def error(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        bark_log = LogObject(
            log_level="ERROR",
            more_data=extra,
            service_name=self.name, code=ERROR,
            msg=msg
        )
        Bark.insert_single_bark_record(bark_log.payload)
        return super().error(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
