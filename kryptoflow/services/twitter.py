import tweepy
from kryptoflow.services.utilities.utils import load_conf
from kryptoflow.models.streamer_base import Streamer
import json
from datetime import datetime
from pprint import pprint
from kryptoflow.services.transforms.sent_analysis import TextAnalyzer, clean_text


def flags(tweet):
    text = tweet['text']
    language = tweet['lang']

    if 'bitcoin gold' in text.lower() or 'BTG' in text.lower():
        return True
    if language != 'en':
        return True

    return False


class TwitterStream(Streamer, tweepy.StreamListener):

    def __init__(self, topic):
        super(TwitterStream, self).__init__(topic=topic)

        consumer_key, consumer_secret, key, secret = load_conf()['twitter'].values()
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(key, secret)
        self._sentence_count = 0
        self._message = {'sentences': [],
                         'polarity': 0,
                         'sentence_count': 0}
        self._last_timestamp = datetime.now().timestamp()
        self.analyzer = TextAnalyzer()

    def stream(self):
        stream = tweepy.Stream(self.auth, self)
        stream.filter(track=['Bitcoin', 'Ethereum', 'Crypto'])

    def start(self):
        self.stream()

    def cache(self):
        pass

    def as_producer(self):
        pass

    def on_data(self, data):
        all_data = json.loads(data)
        text = all_data['text']
        if all_data['user']['followers_count'] > 450:
            if 'extended_tweet' in all_data.keys():
                text = all_data['extended_tweet']['full_text']
            if not flags(all_data):
                text = clean_text(text)
                timestamp = float(all_data['timestamp_ms'])/1000
                self._message['sentences'] += list(self.analyzer.sentences(text))
                self._message['sentence_count'] += len(self._message['sentences'])
                self._message['polarity'] += sum([i['compound'] for i in self.analyzer.sentiment(self._message['sentences'])])

                if timestamp - self.timer.last_timestamp > 5:
                    self.send(self.format_message(self._message))
                    self._release_cache(timestamp)

        return True

    def on_error(self, status):
        print(status)

    def format_message(self, msg):
        msg['sentences'] = ';'.join(msg['sentences'])
        msg.update({'timestamp': self.timer.closest_fith})

        message = {'payload': msg, 'schema': {'type': 'record',
                                              'name': 'tweets',
                                              'fields': [{"field": "sentences", "type": "string"},
                                                         {'field': 'polarity', 'type': 'float'},
                                                         {'field': 'sentence_count', 'type': 'int'},
                                                         {'field': 'timestamp', 'type': 'float'}]
                                              }
                   }
        return msg


if __name__ == '__main__':

    tweet_stream = TwitterStream(topic='twitter')
    tweet_stream.start()

