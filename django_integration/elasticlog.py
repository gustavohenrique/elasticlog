# coding: utf-8
from datetime import datetime
import os

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Index, String, Date
from elasticsearch.connection import RequestsHttpConnection, Urllib3HttpConnection


def fix_date(d):
    try:
        datetime.strptime(d, '%Y-%m-%d')
        return d
    except:
        return ''


class CustomRequestsHttpConnection(RequestsHttpConnection):
    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        timeout = os.environ.get('LOGGO_REQUEST_TIMEOUT')
        return super(CustomRequestsHttpConnection, self).perform_request(method, url, timeout=int(timeout), ignore=ignore)


class CustomUrllib3HttpConnection(Urllib3HttpConnection):
    def __init__(self, host='localhost', port=9200, http_auth=None,
            use_ssl=False, verify_certs=False, ca_certs=None, client_cert=None,
            maxsize=10, **kwargs):

        timeout = os.environ.get('LOGGO_REQUEST_TIMEOUT')
        super(CustomUrllib3HttpConnection, self).__init__(host=host, port=port, timeout=float(timeout),
            http_auth=http_auth, use_ssl=use_ssl, verify_certs=verify_certs,
            ca_certs=ca_certs, client_cert=client_cert, maxsize=maxsize, **kwargs)

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        timeout = os.environ.get('LOGGO_REQUEST_TIMEOUT')
        return super(CustomUrllib3HttpConnection, self).perform_request(method, url, body=body, timeout=float(timeout))


class Log(DocType):
    filename = String(index='analyzed')
    level = String(fields={'raw': String(index='not_analyzed')})
    message = String(analyzer='snowball')
    created_at = Date()


class Loggo(object):

    _instance = None

    def __init__(self, **kwargs):
        self.index = kwargs.get('index')
        self.hosts = kwargs.get('hosts')

        timeout = kwargs.get('timeout', 10)
        os.environ['LOGGO_REQUEST_TIMEOUT'] = str(timeout)

        max_retries = kwargs.get('max_retries', 2)

        connections.create_connection(hosts=self.hosts, connection_class=CustomUrllib3HttpConnection, max_retries=max_retries)
        #connections.create_connection(hosts=self.hosts, connection_class=CustomRequestsHttpConnection, max_retries=max_retries)

        idx = Index(self.index)
        idx.settings(number_of_shards=1, number_of_replicas=1)
        idx.doc_type(Log)

        self.Log = Log

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Loggo, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def insert(self, **kwargs):
        created_at = fix_date(kwargs.get('created_at'))
        log = self.Log(
            filename = kwargs.get('filename'),
            level = kwargs.get('level'),
            message = kwargs.get('message'),
            created_at = created_at
        )
        log.save()
        return log

