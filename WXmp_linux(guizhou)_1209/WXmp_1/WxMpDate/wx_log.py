# -*-coding: utf-8 -*-

import logging as log
from logging import handlers


class WX_log(object):
    LOG_FILE = 'wxmp_log.log'
    handler = log.handlers.TimedRotatingFileHandler(LOG_FILE, when='d', interval=1, backupCount=3)
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = log.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = log.getLogger('wxmplog')
    logger.addHandler(handler)
    logger.setLevel(log.DEBUG)

    def mylog(self, l):
        return self.logger.debug(l)



