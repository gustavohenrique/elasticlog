# conding: utf-8
import json
import falcon

import settings
from .elasticlog import Elasticlog
from .exceptions import ConnectionError, ConnectionTimeout, NotFoundError, ProtocolError
from .customlogger import logger
from .middleware import RequireJSON, JSONTranslator


def execute(req, resp, index_name, method):
    try:
        logger.info('Processing request...')
        method(req, resp, index_name)
    except ConnectionError as ce:
        logger.error(ce)
        raise falcon.HTTPInternalServerError('Connection Error', ce.message)
    except ConnectionTimeout as ct:
        logger.error(ct)
        raise falcon.HTTPInternalServerError('Connection Timeout', ct.message)
    except NotFoundError as ne:
        logger.error(ne)
        raise falcon.HTTPInternalServerError('Index Not Found', ne.message)
    except ProtocolError as pe:
        logger.error(pe)
        raise falcon.HTTPInternalServerError('Error connecting to Elasticsearch', pe.message)
    except Exception as e:
        logger.error(e)
        raise falcon.HTTPBadRequest('Unexpected Error', e.message)


class IndexResource(object):
    def on_get(self, req, resp):
        resp.body = json.dumps({'message': 'It is working!'})

    def on_post(self, req, resp):
        resp.body = json.dumps({'message': 'It is working!'})


class LogResource(object):
    def __init__(self):
        try:
            logger.debug('Connecting to elasticsearch...')
            self.es = Elasticlog(
                hosts = settings.HOSTS,
                timeout = settings.REQUEST_TIMEOUT,
                max_retries = settings.MAX_RETRIES
            )
        except Exception as e:
            logger.error('Error connecting to elasticsearch: %s' % e)

    def on_get(self, req, resp, index_name):
        resp.append_header('Access-Control-Allow-Origin', '*')
        execute(req, resp, index_name, self._search)

    def on_post(self, req, resp, index_name):
        execute(req, resp, index_name, self._insert)

    def _search(self, req, resp, index_name):
        self.es.create_index_if_not_exists(index_name)
        logs = self.es.search(
            index = index_name,
            format = 'dict',
            page = req.get_param_as_int('page'),
            per_page = req.get_param_as_int('per_page'),
            sort = req.get_param('sort'),
            start_date = req.get_param('start_date'),
            end_date = req.get_param('end_date'),
            group_by = req.get_param('group_by')
        )
        count = self.es.count()
        result = {
            'total': count.get('count', 0),
            'items': logs
        }
        resp.body = json.dumps(result)

    def _insert(self, req, resp, index_name):
        data = req.context['doc'] #json.loads(req.stream.read())
        self.es.create_index_if_not_exists(index_name)
        self.es.insert(
            created_at = data.get('created_at'),
            filename = data.get('filename'),
            level = data.get('level'),
            message = data.get('message')
        )
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'status': 'success'})


api = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])
api.add_route('/', IndexResource())
api.add_route('/v1/logs/{index_name}', LogResource())
