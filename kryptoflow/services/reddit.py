import praw
from kryptoflow.services.utilities.utils import load_conf
from kryptoflow.models.streamer_base import Streamer
from kryptoflow.services.transforms.sent_analysis import TextAnalyzer, clean_text
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
        self._last_timestamp = datetime.now().timestamp()
        self._comment_accumulator = {'sentences': [],
                                     'sentence_count': 0,
                                     'polarity': 0}

    def as_producer(self):
        pass

    def cache(self):
        pass

    def accumulate(self, comment):
        sentences = list(self.analyzer.sentences(clean_text(comment.body)))
        self._comment_accumulator['sentences'] += sentences
        self._comment_accumulator['sentence_count'] += len(sentences)
        self._comment_accumulator['polarity'] += sum([i['compound'] for i in
                                                      self.analyzer.sentiment(sentences)])

    def start_stream(self):
        sub_reddit = self.client.subreddit(self.sub_reddits)
        start_time = time()
        self.timer(5, self._send_and_release)
        try:
            for comment in sub_reddit.stream.comments():
                print(comment)
                if comment.created_utc < start_time:
                    continue
                self.accumulate(comment)
        except Exception as e:
            print('ERRROR', e)
            self.start_stream()

    def _send_and_release(self):
        msssg = self.format_message(self._comment_accumulator)
        self.send(msssg)
        self._release_cache()

    def format_message(self, msg):
        msg.update({'ts': str(datetime.fromtimestamp(self.time_util.round_to_nearest())),
                    'sentences': ';'.join(msg['sentences'])})
        return msg


if __name__ == '__main__':
    r = RedditStreamer('reddit')
    r.start_stream()
