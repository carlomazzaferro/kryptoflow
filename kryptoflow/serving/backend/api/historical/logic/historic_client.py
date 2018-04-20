from kryptoflow.common.streamer_base import AvroAsync


def get_historic_data(offset, max_points=50000):
    a = AvroAsync(topic='gdax')
    msgs = a.read_from_offset(offset=offset)
    if len(msgs) > max_points:
        return msgs[max_points:]
    return msgs


def format_data(payload):
    return [{k: v for k, v in i.items() if k in ['price', 'ts']} for i in payload]

