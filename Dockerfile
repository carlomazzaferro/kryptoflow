# docker build -t ubuntu1604py36
FROM python:3.6-stretch

RUN apt-get update
RUN apt-get install -y software-properties-common
# RUN apt-get install -y python-dev
RUN wget -qO - 'https://packages.confluent.io/deb/4.0/archive.key' | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main"
RUN apt-get install -y librdkafka-dev librdkafka1


COPY . kryptoflow
WORKDIR kryptoflow/

RUN mkdir -p ~/tmp/logs
RUN pip3.6 install -r requirements.txt
RUN python3.6 -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
RUN python3.6 setup.py develop

CMD supervisord -c resources/supervisord.conf


