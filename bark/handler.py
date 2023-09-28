import logging
from logging import LogRecord


class BarkHandler(logging.Handler):
    def __init__(self, level: int = 0) -> None:
        super().__init__(level)
        self.records: list[LogRecord] = []
    
    def emit(self, record: LogRecord) -> None:
        self.records.append(record)

class HandlerObject:
    handler: BarkHandler = None

handler_object = HandlerObject()
