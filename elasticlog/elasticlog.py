# coding: utf-8
import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index, Search

import utils
from models import LogType, Log
from connections import CustomUrllib3HttpConnection


class Elasticlog(object):

    _instance = None

    def __init__(self, **kwargs):
        self.hosts = kwargs.get('hosts', 'localhost')
        self.client = Elasticsearch(self.hosts)

        timeout = kwargs.get('timeout', 10)
        os.environ['LOGGO_REQUEST_TIMEOUT'] = str(timeout)

        max_retries = kwargs.get('max_retries', 2)
        connections.create_connection(hosts=self.hosts, connection_class=CustomUrllib3HttpConnection, max_retries=max_retries)

        index_name = kwargs.get('index', None)
        self.create_index_if_not_exists(index_name)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Elasticlog, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def create_index_if_not_exists(self, index_name):
        self.index = index_name
        idx = Index(index_name)
        idx.settings(number_of_shards=1, number_of_replicas=1)
        idx.doc_type(LogType)
        try:
            idx.create()
        except:
            pass

    def insert(self, **kwargs):
        created_at = utils.fix_date(kwargs.get('created_at'))
        log_type = LogType(
            filename = kwargs.get('filename'),
            level = kwargs.get('level'),
            message = kwargs.get('message'),
            created_at = created_at
        )
        return log_type.save()

    def search(self, **params):
        index = params.get('index', self.index)
        search = Search(using=self.client, index=index)

        page = params.get('page', None)
        per_page = params.get('per_page', None)
        if page and per_page:
            page = page - 1
            search._extra = {'from': page, 'size': per_page}

        sort = params.get('sort', None)
        if sort and sort.replace('-', '') in ['created_at', 'level']:
            search = search.sort(sort)

        date_filter = self._filter_by_date_interval(params)
        if date_filter:
            search = search.filter(date_filter)

        level = params.get('group_by', None)
        if level:
            search = search.query('match', level=level)

        hits = search.execute()

        format = params.get('format', 'object')
        if format == 'dict':
            return self._to_dict(hits)
        else:
            return self._to_logs(hits)

    def count(self):
        response = self.client.count(index=self.index)
        return response

    def _to_logs(self, hits):
        logs = []
        for hit in hits:
            log = Log()
            log.id = hit.meta.id
            log.filename = hit.filename
            log.level = hit.level
            log.message = hit.message
            log.created_at = utils.to_datetime(hit.created_at, '%Y-%m-%d')
            logs.append(log)
        return logs

    def _to_dict(self, hits):
        results = []
        for hit in hits:
            d = {
                'id': hit.meta.id,
                'filename': hit.filename,
                'level': hit.level,
                'message': hit.message,
                'created_at': hit.created_at
            }
            results.append(d)
        return results

    def _filter_by_date_interval(self, params):
        start_date = params.get('start', None)
        end_date = params.get('end', None) #str(utils.today()))
        if start_date:
            d1 = utils.to_datetime(start_date)
            d2 = utils.to_datetime(end_date)
            if d1 and d2:
                return {'range': {
                    'created_at': { 'gte': str(d1).replace(' ', 'T'), 'lte': str(d2).replace(' ', 'T') }
                }}
        return None
