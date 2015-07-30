# coding: utf-8
import sys
import logging

import settings


logFormatter = logging.Formatter('%(asctime)s [%(levelname)-5.5s]  %(message)s')
logger = logging.getLogger()

fileHandler = logging.FileHandler('{0}'.format(settings.LOG_FILE_PATH))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)