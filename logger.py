import logging
from config import config
from pythonjsonlogger import jsonlogger

level = getattr(logging, config['log']['level'].upper())
logging.basicConfig(filename=config['log']['file'], level=level)
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
