# coding: utf-8
import os

from elasticsearch.connection import RequestsHttpConnection, Urllib3HttpConnection


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
