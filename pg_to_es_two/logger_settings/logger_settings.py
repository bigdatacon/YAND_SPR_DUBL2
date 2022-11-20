import logging
import time
logger = logging.getLogger(__name__)

"""tune logger for console write"""
#1 create logger
logger = logging.getLogger('backoff_logging')
logger.setLevel(logging.DEBUG)

#2 create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

#3 create formatter
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s-%(asctime)s ')

#4 add formatter to ch
ch.setFormatter(formatter)

#5 add ch to logger
logger.addHandler(ch)

# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')