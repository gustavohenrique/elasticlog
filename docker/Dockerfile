FROM elasticsearch
MAINTAINER Gustavo Henrique <gustavo@gustavohenrique.net>

ADD requirements.txt /tmp/requirements.txt
ADD add_initial_data.sh /tmp/add_initial_data.sh

RUN /bin/bash -c "apt-get update && apt-get install nginx python python-setuptools -y"
RUN /bin/bash -c "easy_install pip && pip install -r /tmp/requirements.txt"
RUN plugin -i elasticsearch/marvel/latest

ADD default-site-enabled-nginx /etc/nginx/sites-enabled/default

EXPOSE 9200
EXPOSE 8000
EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD service nginx start && elasticsearch -d && while true; do sleep 1; done
