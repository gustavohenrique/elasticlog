default: docker-test

install:
	@pip install -r requirements.txt

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@docker rm -f elasticlog > /dev/null 2> /dev/null || true

build: clean
	@cd docker && docker build -t=elasticlog .

docker-run:
	@docker run -d -p 9200:9200 -p 8000:8000 -p 80:80 --hostname elasticlog --name elasticlog -v ${PWD}:/app elasticlog
	@echo "Waiting for 10s until the Elasticsearch starts..."
	@sleep 10

fixtures:
	@echo "Inserting initial data..."
	@docker exec elasticlog /tmp/add_initial_data.sh

run:
	@docker exec -ti elasticlog python /app/server.py

test: docker
	@docker exec elasticlog python /app/elasticlog/test_elasticlog.py

enter:
	@docker exec -ti elasticlog bash

