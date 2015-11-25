FROM elasticsearch
MAINTAINER Gustavo Henrique <gustavo@gustavohenrique.net>

ADD requirements.txt /tmp/requirements.txt

RUN /bin/bash -c "apt-get update && apt-get install python python-setuptools -y"
RUN /bin/bash -c "easy_install pip && pip install -r /tmp/requirements.txt"

EXPOSE 9200 9300

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD elasticsearch -d; sleep 10; python /app/test_loggo.py

