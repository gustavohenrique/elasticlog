# coding: utf-8
from datetime import datetime


DATE_PATTERN = '%Y-%m-%dT%H:%M:%S'

def fix_date(str):
    try:
        datetime.strptime(str, DATE_PATTERN)
        return str
    except:
        return ''

def to_datetime(str, pattern=None):
    try:
        if not pattern:
            pattern = DATE_PATTERN
        return datetime.strptime(str, pattern)
    except:
        return None

def today():
    datetime.strftime(datetime.now(), DATE_PATTERN)
