Elasticlog
---
> A RESTful API to store and search log data in Elasticsearch

[![Demo](https://github.com/gustavohenrique/elasticlog/raw/master/screenshot.png)](http://github.com/gustavohenrique/elasticlog)


First, you need to send the log's data to storage in Elasticsearch. You can configure any app to that just making a `POST` to Elasticlog. You need to configure an Elasticsearch server too and change the hostname variable defined into `settings.py` file.

## Running

```bash
git clone <this-repo>
pip install -r requirements.txt
python server.py
```

You can run using the Docker way:

```bash
make build
make docker-run
make fixtures
make run
```

To send the log's data, just make a `POST` to the API:

```bash
curl -X POST -H 'content-type:application/json' http://`boot2docker ip`/v1/logs/index1 -d '{
    "created_at": "2015-07-30",
    "filename": "connection.py",
    "level": "ERROR",
    "message": "Error connecting to database"
}'
```

The API can also list all log's data:

```bash
# basic usage
curl -H 'content-type:application/json' http://`boot2docker ip`/v1/logs/index1

# pagination support
curl -H 'content-type:application/json' http://`boot2docker ip`/v1/logs/index1?page=1&per_page=5

# order by asc or desc
curl -H 'content-type:application/json' http://`boot2docker ip`/v1/logs/index1?sort=-created_at

# group by level
curl -H 'content-type:application/json' http://`boot2docker ip`/v1/logs/index1?group_by=ERROR
```

## Frontend

There is a web interface to see the log's data.

```bash
open http://`boot2docker ip`/index.html
```

## More

The `Marvel` plugin is installed into Docker instance. You can access by:

```bash
open http://`boot2docker ip`:9200/_plugin/marvel
```

## License

MIT
