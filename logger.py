import logging
from config import config
from pythonjsonlogger import jsonlogger

level = getattr(logging, config['log']['level'].upper())
logger = logging.getLogger()
logger.setLevel(level)

streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler(config['log']['file'])

formatter = jsonlogger.JsonFormatter()
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

logging.getLogger("peewee").setLevel(logging.WARNING)
