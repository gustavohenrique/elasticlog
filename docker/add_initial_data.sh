#!/bin/bash
host="http://localhost:9200"
index="index1"
type="log"

curl -X POST "$host/$index/$type" -d '{"created_at":"2015-01-10", "filename": "views", "level": "ERROR", "message": "elasticsearch.exceptions.ConnectionError: ConnectionError"}'
curl -X POST "$host/$index/$type" -d '{"created_at":"2015-01-02", "filename": "custom_views", "level": "ERROR", "message": "NameError: name request is not defined"}'
curl -X POST "$host/$index/$type" -d '{"created_at":"2015-04-04", "filename": "models", "level": "DEBUG", "message": "AttributeError: str object has no attribute xpto"}'
curl -X POST "$host/$index/$type" -d '{"created_at":"2015-02-21", "filename": "core.views", "level": "INFO", "message": "IndexError: list index out of range"}'
curl -X POST "$host/$index/$type" -d '{"created_at":"2015-03-08", "filename": "util", "level": "DEBUG", "message": "MissingSchema: Invalid URL gustavo: No schema supplied. Perhaps you meant http://gustavo?"}'
curl -X POST "$host/$index/$type" -d '{"created_at":"2015-02-01", "filename": "api.views", "level": "ERROR", "message": "ERROR:django.request:Internal Server Error"}'
