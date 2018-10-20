from kafka_tfrx.stream import KafkaStream

from kryptoflow.scrapers.reddit import RedditStreamer
from kryptoflow.managers.project import ProjectManager

if __name__ == '__main__':
    schemas = ProjectManager.get_value('kafka')['schemas']
    secrets = ProjectManager.get_secrets('reddit')
    sink = KafkaStream.avro_producer(schemas=schemas, topic='reddit')
    r = RedditStreamer(producer=sink, reddit_config=secrets)
    r.start_stream()