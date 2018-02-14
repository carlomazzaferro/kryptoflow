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
        self._tweet_accumulator = {'sentences': [],
                                   'sentence_count': 0,
                                   'polarity': 0}

    def start(self):
        stream = tweepy.Stream(self.auth, self)
        stream.filter(track=['Bitcoin', 'Ethereum', 'Crypto'])

    def stream_start(self):
        self.timer(5, self._send_and_release)
        self.start()

    def cache(self):
        pass

    def as_producer(self):
        pass

    def accumulate(self, text):
        sentences = list(self.analyzer.sentences(text))
        self._tweet_accumulator['sentences'] += sentences
        self._tweet_accumulator['sentence_count'] += len(sentences)
        self._tweet_accumulator['polarity'] += sum([i['compound'] for i in
                                                      self.analyzer.sentiment(sentences)])

    def _send_and_release(self):
        msssg = self.format_message(self._tweet_accumulator)
        self.send(msssg)
        self._release_cache()

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

        self.accumulate(clean_text(text))

    def on_error(self, status):
        print(status)

    def format_message(self, msg):
        msg['sentences'] = ';'.join(msg['sentences'])
        msg.update({'timestamp': self.time_util.round_no_nearest()})
        return msg


if __name__ == '__main__':

    tweet_stream = TwitterStream(topic='twitter')
    tweet_stream.stream_start()

