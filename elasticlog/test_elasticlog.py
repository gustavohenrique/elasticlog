# coding: utf-8
import unittest
import time
import os

from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search, Q, Index

from elasticlog import Elasticlog

HOST = os.environ.get('TEST_HOST', 'localhost')
INDEX_NAME = 'index1'

def fixtures():
    TYPE = 'log_type'
    bulk_data = [
        {'_source': {'created_at':'2015-01-10', 'filename': 'views', 'level': 'ERROR', 'message': 'elasticsearch.exceptions.ConnectionError: ConnectionError'}, '_index': INDEX_NAME, '_type': TYPE},
        {'_source': {'created_at':'2015-01-02', 'filename': 'custom_views', 'level': 'ERROR', 'message': 'NameError: name "request" is not defined'}, '_index': INDEX_NAME, '_type': TYPE},
        {'_source': {'created_at':'2015-04-04', 'filename': 'models', 'level': 'DEBUG', 'message': 'AttributeError: "str" object has no attribute "xpto"'}, '_index': INDEX_NAME, '_type': TYPE},
        {'_source': {'created_at':'2015-02-21', 'filename': 'core.views', 'level': 'INFO', 'message': 'IndexError: list index out of range'}, '_index': INDEX_NAME, '_type': TYPE},
        {'_source': {'created_at':'2015-03-08', 'filename': 'util', 'level': 'DEBUG', 'message': 'MissingSchema: Invalid URL "gustavo": No schema supplied. Perhaps you meant http://gustavo?'}, '_index': INDEX_NAME, '_type': TYPE},
        {'_source': {'created_at':'2015-02-01', 'filename': 'api.views', 'level': 'ERROR', 'message': 'ERROR:django.request:Internal Server Error'}, '_index': INDEX_NAME, '_type': TYPE}
    ]
    es = Elasticsearch(hosts=[HOST])
    helpers.bulk(es, bulk_data)
    time.sleep(2)


class TestElasticlog(unittest.TestCase):

    def setUp(self):
        self.es = Elasticlog(hosts=[HOST], index=INDEX_NAME)

    def tearDown(self):
        Index(INDEX_NAME).delete()

    def test_should_insert_data(self):
        inserted = self.es.insert(filename='views.py', level='error', created_at='2015-07-18', message='object not found')
        self.assertTrue(inserted)

    def test_should_insert_empty_date_if_it_is_invalid(self):
        inserted = self.es.insert(filename='views.py', level='error', created_at='invalid', message='object not found')
        self.assertTrue(inserted)

    def test_should_list_the_first_ten(self):
        fixtures()

        logs = self.es.search()
        self.assertEquals(6, len(logs))

        log = logs[0]
        self.assertTrue(len(log.id) > 0)
        self.assertEquals(log.level, 'ERROR')
        self.assertEquals(log.filename, 'views')
        self.assertEquals(log.message, 'elasticsearch.exceptions.ConnectionError: ConnectionError')

    def test_should_paginate_the_result(self):
        fixtures()

        logs = self.es.search(page=1, per_page=2)
        self.assertEquals(2, len(logs))

        log = logs[0]
        self.assertTrue(len(log.id) > 0)
        self.assertEquals(log.level, 'ERROR')
        self.assertEquals(log.filename, 'views')
        self.assertEquals(log.message, 'elasticsearch.exceptions.ConnectionError: ConnectionError')

    def test_should_sort_asc(self):
        fixtures()
        logs = self.es.search(sort='created_at')
        log = logs[0]
        self.assertEquals(str(log.created_at), '2015-01-02 00:00:00')
        self.assertEquals(log.level, 'ERROR')
        self.assertEquals(log.filename, 'custom_views')
        self.assertEquals(log.message, 'NameError: name "request" is not defined')

    def test_should_sort_desc(self):
        fixtures()
        logs = self.es.search(sort='-created_at')
        log = logs[0]
        self.assertEquals(str(log.created_at), '2015-04-04 00:00:00')
        self.assertEquals(log.level, 'DEBUG')
        self.assertEquals(log.filename, 'models')
        self.assertEquals(log.message, 'AttributeError: "str" object has no attribute "xpto"')

    def test_should_filter_by_date_interval(self):
        fixtures()
        logs = self.es.search(start='2015-01-01T00:00:00', end='2015-02-21T00:00:00')
        self.assertEquals(4, len(logs))

        log = logs[0]
        self.assertEquals(str(log.created_at), '2015-01-10 00:00:00')
        self.assertEquals(log.level, 'ERROR')
        self.assertEquals(log.filename, 'views')
        self.assertEquals(log.message, 'elasticsearch.exceptions.ConnectionError: ConnectionError')

    def test_should_raises_exception_if_pass_an_invalid_date_interval(self):
        fixtures()
        try:
            logs = self.es.search(start='invalid', end='2015-02-21')
            fail()
        except:
            pass

    def test_should_count_the_total_of_logs(self):
        fixtures()
        response = self.es.count()
        self.assertEquals(response.get('count'), 6)


class TestTimeoutElasticlog(unittest.TestCase):

    def test_should_abort_if_waiting_for_long_time(self):
        es = Elasticlog(hosts=['172.17.0.254'], index='loggo', timeout=1, max_retries=0)
        try:
            es.insert(filename='views.py', level='error', created_at='invalid', message='object not found')
            fail()
        except:
            pass


if __name__ == '__main__':
    unittest.main()
