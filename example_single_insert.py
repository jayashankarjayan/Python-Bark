import logging

from bark import Bark

logging.basicConfig(level=logging.DEBUG)

logger = Bark(__name__)

try:
    logger.info("This is a info log")
    _ = 1/ 0 # deliberately creating an exception
except Exception as why:
    logger.error("This is a error log, with some extra data: %s", why, extra={"Hello": "World"})
    logger.debug("This is a debug log")
    logger.warning("This is a warning log")
