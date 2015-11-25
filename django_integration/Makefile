default: docker-test

install:
	@pip install -r requirements.txt

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf

docker-test:
	@docker build -t=loggo .
	@docker run --rm -v ${PWD}:/app loggo

test: clean
	@python test_loggo.py

