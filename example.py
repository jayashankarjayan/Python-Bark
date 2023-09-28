import logging
from bark import bark
from bark.handler import BarkHandler

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

bark_handler = BarkHandler()
logger.addHandler(bark_handler)

formatter = logging.Formatter('%(asctime)s %(Metadata)s : %(message)s')
bark_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

@bark(logger)
def my_func(a: int, b: int):
    logger.info("INFO  Log", extra={"Metadata": "A"})
    logger.warning("DEBUG  Log", extra={"Metadata": "B"})
    return "s"


if __name__ == "__main__":
    my_func(1, b=2)