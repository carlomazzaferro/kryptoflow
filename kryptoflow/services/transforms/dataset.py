import json
import pandas


class Dataset(object):

    file_path = '/media/carlo/HDD/kafka_local/'

    def __init__(self, from_file=True):
        self.gdax_path = self.file_path + 'gdax.txt'
        self.twitter_path = self.file_path + 'twitter.txt'
        self.reddit_path = self.file_path + 'reddit.txt'

    def load_df(self, path, keep_keys=['ts']):
        rows = []
        with open(path) as inf:
            for row in inf:
                row_dict = json.loads(row)
                rows.append({k: v for k, v in row_dict.items() if k in keep_keys})
        df = pandas.DataFrame(rows)
        df['ts'] = pandas.to_datetime(df['ts'])
        df['time_diff'] = df['ts'].diff().dt.seconds.div(1, fill_value=0)
        return df

if __name__ == '__main__':
    d = Dataset()
    df = d.load_df(d.gdax_path, keep_keys=['ts', 'price', 'volume_24h',
                                           'spread'])

