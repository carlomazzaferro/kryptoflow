import wget
import os
import gzip
import shutil
import csv
import psycopg2
import argparse
import sys
from datetime import datetime, timedelta
import pandas


def connection(host, db, uname, pw):
    conn = psycopg2.connect(database=db, user=uname, host=host, password=pw)
    return conn.cursor()


def parse_args(args):
    parser = argparse.ArgumentParser(description='Process submissions')
    parser.add_argument('--uname', '-U', default='user')
    parser.add_argument('--pw', '-p', default='')
    parser.add_argument('--host', '-H', default='localhost')
    parser.add_argument('-db', default='kryptoflow')
    return parser.parse_args(args)


class Validator(object):

    def __init__(self, cursor):
        self.url = 'https://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz'
        self.in_gz = '~/tmp/coinbaseUSD.csv.gz'
        self.out_csv = '~/tmp/coinbase.csv'
        self.curs = cursor

    def download(self):
        wget.download(self.url, out=os.path.expanduser(self.in_gz))

    def load(self):
        with gzip.open(os.path.expanduser(self.in_gz), 'rb') as f_in:
            with open(os.path.expanduser(self.out_csv), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        with open(os.path.expanduser(self.out_csv), 'r') as cb:
            reader = csv.reader(cb)
            relevant = []
            for i, row in enumerate(reader):
                if i % 5E5 == 0:
                    print(i)  # some logging
                if i < 36E6:  # around where records from when I started recording data actually start
                    continue
                if datetime.fromtimestamp(float(row[0])) < datetime(year=2018, month=2, day=17):
                    continue
                else:
                    relevant.append([float(i) for i in row])

        with open(os.path.expanduser(self.out_csv), 'w') as out:
            writer = csv.writer(out)
            writer.writerow(['time', 'price', 'amount'])
            writer.writerows(relevant)

    def determine_missing_values(self):
        self.curs.execute(
            """SELECT ts FROM public.gdax"""
        )
        rows = [datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S') for i in cursor.fetchall()]

        first, last = rows[0], rows[-1]
        date_list = self.range_of_dates(first, last)
        return set(set(date_list)).difference(rows)

    @staticmethod
    def range_of_dates(start, end):
        dates = []
        date = start
        while date < end:
            dates.append(date)
            date += timedelta(seconds=5)

        return dates


class Historical(object):

    def __init__(self):
        self.out_csv = '~/tmp/coinbase.csv'
        self.loaded_df = pandas.read_csv(self.out_csv)
        self.loaded_df['time'] = self.loaded_df['time'].apply(lambda x: datetime.fromtimestamp(x))

    @property
    def df(self):
        return self.loaded_df

    def find_closest(self, date):
        return self.df.ix[(self.df['time']-date).abs().argsort()[:10]]

    def hourly_range(self, date):
        return self.df[(self.df['time'] > (date - timedelta(hours=12))) &
                       (self.df['time'] < date + timedelta(hours=12))]['amount']

    def calc_spread(self, date):
        mini = self.find_closest(date)
        spread = (max(mini['price']) - min(mini['price']))/(len(mini)/2)
        return spread if spread > 0.01 else 0.01

    def find_avg_closest(self, other):
        other_df = self.find_closest(other)
        daily_volume = self.hourly_range(other)
        spread = self.calc_spread(other)
        price = other_df['price'].mean()
        volume = daily_volume.sum()
        return price, volume, other, spread


if __name__ == '__main__':
    _args = parse_args(sys.argv[1:])
    # print(_args)
    cursor = connection(_args.host, _args.db, _args.uname, _args.pw)
    val = Validator(cursor)
    missing_values = val.determine_missing_values()
    print(len(missing_values))

    hist = Historical()
    print(hist.df)
    for i, missing in enumerate(missing_values):
        print(hist.find_avg_closest(missing))
        print(missing, i)
        print()
