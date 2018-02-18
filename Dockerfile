# docker build -t ubuntu1604py36
FROM python:3.6-stretch

RUN apt-get update -y && apt-get install -y software-properties-common \
       && wget -qO - 'https://packages.confluent.io/deb/4.0/archive.key' | apt-key add - \
       && add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main" \
       && apt-get install -y librdkafka-dev librdkafka1

COPY . kryptoflow
WORKDIR kryptoflow/
RUN mkdir -p ~/tmp/logs

#  RUN bash resources/kryptoflow_setup_script.sh
RUN pip3.6 install -r requirements.txt
RUN python3.6 -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
RUN python3.6 setup.py develop

# CMD supervisord -c resources/supervisord.conf


