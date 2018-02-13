import praw
import json
import pymongo
from kryptoflow.services.utilities.utils import load_conf
from kryptoflow.models.streamer_base import Streamer
from pprint import pprint
from kryptoflow.services.transforms.sent_analysis import TextAnalyzer
from datetime import datetime
from time import time


class RedditStreamer(Streamer):

    sub_reddits = '+'.join([
        'Bitcoin',
        'btc',
        'CyptoCurrency',
        'BitcoinMarkets',
        'ethtrader',
        'cryptomarkets',
        'BitcoinBeginners'
    ])

    def __init__(self, topic):
        super().__init__(topic=topic)
        self.client = praw.Reddit(**load_conf()['reddit'])
        self.analyzer = TextAnalyzer()
        self._sentence_count = 0
        self._message = {'sentences': [],
                         'polarity': 0,
                         'sentence_count': 0}
        self._last_timestamp = datetime.now().timestamp()

    def as_producer(self):
        pass

    def cache(self):
        pass

    def start(self):
        self.stream()

    def stream(self):
        sub_reddit = self.client.subreddit(self.sub_reddits)
        start_time = time()
        for comment in sub_reddit.stream.comments():
            if comment.created_utc < start_time:
                continue

            timestamp = comment.created
            self._message['sentences'] += list(self.analyzer.sentences(comment.body))
            self._message['sentence_count'] += len(self._message['sentences'])
            self._message['polarity'] += sum([i['compound'] for i in self.analyzer.sentiment(self._message['sentences'])])

            if timestamp - self._last_timestamp > 5:
                self.send(self.format_message(self._message))
                self._release_cache(timestamp)

    def format_message(self, msg):
        msg.update({'timestamp': self.timer.closest_fith})

        msg['sentences'] = ';'.join(msg['sentences'])

        message = {'payload': msg, 'schema': {'type': 'record',
                                              'name': 'reddit_comments',
                                              'fields': [{"field": "sentences", "type": "string"},
                                                         {'field': 'polarity', 'type': 'float'},
                                                         {'field': 'sentence_count', 'type': 'int'},
                                                         {'field': 'timestamp', 'type': 'float'}]
                                              }
                   }
        from pprint import pprint
        pprint(message)
        return message


if __name__ == '__main__':
    r = RedditStreamer('reddit')
    r.start()
