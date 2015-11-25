# coding: utf-8
from django.conf import settings

from datetime import datetime
import time
import logging

from django_loggo.loggo import Loggo


class LoggoHandler(logging.Handler):

    def __init__(self):
        super(LoggoHandler, self).__init__()

    def handle(self, record):
        try:
            config = settings.LOGGO

            hosts = config.get('hosts', ['localhost'])
            index = config.get('index')
            timeout = config.get('timeout', 5)
            max_retries = config.get('max_retries', 1)

            created_at_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
            created_at_date = datetime.strptime(created_at_time, '%Y-%m-%d %H:%M:%S')

            es = Loggo(hosts=hosts, index=index, timeout=timeout, max_retries=max_retries)
            es.insert(filename=record.name, level=record.levelname, message=record.msg, created_at=created_at_date)
        except Exception as e:
            logging.getLogger().error('loggo: %s' % e.message)

