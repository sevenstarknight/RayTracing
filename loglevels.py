from loguru import logger
import sys

class SetLevel():
    """Set the levels for operations
    """
    def __init__(self, level:str):
        """LOGURU initialization for set levels

        Args:
            level (str): what levels?
        """
        self.level = level.upper()
        if self.validateLogLevel():
            self.setLevel()
        
    def setLevel(self):
        """Set the levels
        """
        logger.remove() #removes configuration for the default handler "0" is the default ID number
        logger.add(sys.stderr, level=self.level) #only records logs with a severity of Warning and greater

    def validateLogLevel(self, correct:bool=True) -> bool:
        """Validate the logs

        Args:
            correct (bool, optional): yes valid. Defaults to True.

        Returns:
            bool: correct?
        """
        if self.level not in ["DEBUG", "TRACE", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]:
            correct = False
        return correct