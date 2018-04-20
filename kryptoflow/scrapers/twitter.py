import tweepy
from kryptoflow.scrapers.utilities.utils import load_conf
from kryptoflow.common.streamer_base import AvroAsync
import json
from datetime import datetime
from kryptoflow.scrapers.transforms.sent_analysis import TextAnalyzer, clean_text


def flags(tweet):
    text = tweet['text']
    language = tweet['lang']

    if 'bitcoin gold' in text.lower() or 'BTG' in text.lower():
        return True
    if language != 'en':
        return True

    return False


class TwitterStream(tweepy.StreamListener):

    def __init__(self, producer=None):
        super(TwitterStream, self).__init__()
        self.topic = 'twitter'
        consumer_key, consumer_secret, key, secret = load_conf()['twitter'].values()
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(key, secret)
        self.analyzer = TextAnalyzer()

        self.producer = producer

    def start(self):
        stream = tweepy.Stream(self.auth, self)
        stream.filter(track=['Bitcoin', 'Ethereum', 'Crypto'])

    def on_data(self, data):
        all_data = json.loads(data)
        text = all_data['text']
        if flags(all_data):
            return None
        if all_data['user']['followers_count'] > 450:
            if 'extended_tweet' in all_data.keys():
                text = all_data['extended_tweet']['full_text']

        if len(text) < 5:
            return None

        all_data['text'] = clean_text(text)
        message = self.format_message(all_data)
        print(message)
        self.producer.produce(topic=self.topic, value=message)

    def on_error(self, status):
        print('Error %s' % status)
        self.start()

    def format_message(self, msg):
        sentences = list(self.analyzer.sentences(msg['text']))
        sentence_count = len(sentences)
        polarity = sum([i['compound'] for i in self.analyzer.sentiment(sentences)])

        message = {'sentences': str(msg['text']),
                   'polarity': polarity,
                   'sentence_count': sentence_count,
                   'ts':  str(
                       datetime.fromtimestamp(
                           int(msg['timestamp_ms'])/1000).replace(microsecond=0)
                   ),
                   }
        return message


if __name__ == '__main__':
    sink = AvroAsync(topic='reddit')
    tweet_stream = TwitterStream(producer=sink.producer())
    tweet_stream.start()

