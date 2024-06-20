import sys

from loguru import logger

class TestUtilities():

    def __init__(self) -> None:
        logger.remove()
        logger.add(sys.stderr, level="WARNING")