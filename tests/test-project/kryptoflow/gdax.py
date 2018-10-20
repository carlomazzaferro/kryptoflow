from kafka_tfrx.stream import KafkaStream
from kryptoflow.scrapers.gdax_ws import GDAXClient
from kryptoflow.managers.project import ProjectManager

if __name__ == '__main__':

    schemas = ProjectManager.get_value('kafka')['schemas']
    sink = KafkaStream.avro_producer(topic='gdax', ip='localhost', schemas=schemas)
    gd = GDAXClient(products=['BTC-USD'], channels=['ticker'], producer=sink)
    gd.start_stream()
