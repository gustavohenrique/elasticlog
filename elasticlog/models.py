# coding: utf-8
from elasticsearch_dsl import DocType, String, Date


class LogType(DocType):
    filename = String(index='analyzed')
    level = String(fields={'raw': String(index='not_analyzed')})
    message = String(analyzer='snowball')
    created_at = Date()

    def __unicode__(self):
        return u'%s %s' % (self.created_at, self.message)


class Log(object):
    id = None
    filename = None
    level = None
    message = None
    created_at = None

    def __unicode__(self):
        return u'%s %s' % (self.created_at, self.message)
