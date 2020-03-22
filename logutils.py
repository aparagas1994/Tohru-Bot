from logging.handlers import TimedRotatingFileHandler
import logging

APP_NAME = 'Tohru'

def setup_log():
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler("logs/application.log", when="h", interval=1, backupCount=24)
    formatter = logging.Formatter('%(asctime)s %(filename)s [%(levelname)s] pid(%(process)d): %(message)s')


    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_log()