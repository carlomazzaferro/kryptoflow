import praw
from kryptoflow.scrapers.transforms.sent_analysis import TextAnalyzer
from datetime import datetime
from time import time


class RedditStreamer(object):

    sub_reddits = '+'.join([
        'Bitcoin',
        'btc',
        'CyptoCurrency',
        'BitcoinMarkets',
        'ethtrader',
        'cryptomarkets',
        'BitcoinBeginners'
    ])

    def __init__(self, producer=None, reddit_config=None):
        client_id = reddit_config['client_id']
        client_secret = reddit_config['client_secret']
        user_agent = reddit_config['user_agent']
        self.client = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.analyzer = TextAnalyzer()
        self.producer = producer
        self.topic = 'reddit'

    def start_stream(self):
        sub_reddit = self.client.subreddit(self.sub_reddits)
        start_time = time()
        try:
            for comment in sub_reddit.stream.comments():
                if comment.created_utc < start_time:
                    continue
                message = self.format_message(comment)
                for k, v in message.items():
                    print(k, v, type(k), type(v))
                self.producer.produce(topic=self.topic, value=message)
        except Exception as e:
            print('ERROR', e)
            self.start_stream()

    def format_message(self, msg):
        sentences = list(self.analyzer.sentences(msg.body))
        sentence_count = len(sentences)
        polarity = sum([i['compound'] for i in self.analyzer.sentiment(sentences)])

        message = {'sentences': msg.body,
                   'polarity': polarity,
                   'sentence_count': sentence_count,
                   'ts':  str(datetime.fromtimestamp(msg.created_utc).replace(microsecond=0)),
                   }
        print(message)
        return message

