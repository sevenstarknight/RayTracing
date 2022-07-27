import logging
import sys

APP_LOGGER_NAME = "simulation"

def get_logger(module_name):    
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)

def setup_applevel_logger(file_name=None):

    logger = logging.getLogger(APP_LOGGER_NAME)
    logger.setLevel(logging.INFO)
 
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(sh)

    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        logger.addHandler(fh)

    return logger