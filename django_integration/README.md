django_loggo
============

> A logger handler to send messages to loggo elasticsearch

## Install

```bash
pip install django_loggo
```

## Setup

Open your `settings` file and put:

```
INSTALLED_APPS += ('django_loggo',)

LOGGO = {
    'hosts': ['172.17.0.1'],
    'index': 'futebolapi',
    'timeout': 2,
    'max_retries': 1
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(module)s - %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'loggo': {
            'class': 'django_loggo.handler.LoggoHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'core': {
            'handlers': ['loggo','console'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
```

## Testing

You can run the tests into container:

```bash
make docker-test
```

It is possible to use the elasticsearch API:

```bash
curl http://<host>:9200/<index>/_search?pretty=true
```

## License

MIT
