from kafka_tfrx.stream import KafkaStream

from kryptoflow.scrapers.twitter import TwitterStream
from kryptoflow.managers.project import ProjectManager


if __name__ == '__main__':
    schemas = ProjectManager.get_value('kafka')['schemas']
    secrets = ProjectManager.get_secrets('twitter')

    sink = KafkaStream.avro_producer(schemas=schemas, topic='reddit')
    tweet_stream = TwitterStream(producer=sink, twitter_config=secrets)
    tweet_stream.start()
