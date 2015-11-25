# coding: utf-8
import unittest
import time

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, Index

from loggo import Loggo


class TestLoggo(unittest.TestCase):

    def setUp(self):
        self.es = Loggo(hosts=['172.17.0.26'], index='loggo')
        #Index('loggo').delete(ignore=404)

    def test_should_insert_data(self):
        self.es.insert(filename='views.py', level='error', created_at='2015-07-18', message='object not found')
        hits = self._search(filename='views.py')

        hit = hits[0]
        id = hit.meta.id
        self.assertTrue(len(id) > 0)

    def test_should_insert_empty_date_if_it_is_invalid(self):
        self.es.insert(filename='views.py', level='error', created_at='invalid', message='object not found')
        hits = self._search(filename='views.py')

        hit = hits[0]
        id = hit.meta.id
        self.assertTrue(len(id) > 0)

    def _search(self, **kwargs):
        time.sleep(3)
        es = Elasticsearch(self.es.hosts)
        s = Search(using=es, index=self.es.index).filter('term', filename=kwargs.get('filename'))
        return s.execute()


class TestTimeoutLoggo(unittest.TestCase):

    def test_should_abort_if_waiting_for_long_time(self):
        es = Loggo(hosts=['172.17.0.254'], index='loggo', timeout=1, max_retries=0)
        try:
            es.insert(filename='views.py', level='error', created_at='invalid', message='object not found')
            fail()
        except:
            pass


if __name__ == '__main__':
    unittest.main()

