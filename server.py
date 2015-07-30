# conding: utf-8
from wsgiref import simple_server

from elasticlog.api import api


if __name__ == '__main__':
    print 'Server running on port 8000'
    httpd = simple_server.make_server('0.0.0.0', 8000, api)
    httpd.serve_forever()

