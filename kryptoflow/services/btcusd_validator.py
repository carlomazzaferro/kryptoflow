import wget
import os
import gzip
import csv
from datetime import datetime


def download():
    url = 'https://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz'
    wget.download(url, out=os.path.expanduser('~/tmp/coinbase.csv.gz'))

def load():
    import gzip
    import shutil
    with gzip.open(os.path.expanduser('~/tmp/coinbase.csv.gz'), 'rb') as f_in:
        with open(os.path.expanduser('~/tmp/coinbase.csv'), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    with open(os.path.expanduser('~/tmp/coinbase.csv'), 'r') as cb:
        reader = csv.reader(cb)
        relevant = []
        for i, row in enumerate(reader):
            if i % 5E5 == 0:
                print(i)
            if i < 36E6:
                continue
            if datetime.fromtimestamp(float(row[0])) < datetime(year=2018, month=2, day=17):
                continue
            else:
                relevant.append([float(i) for i in row])

    with open(os.path.expanduser('~/tmp/coinbase1.csv'), 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['time', 'price', 'amout'])
        writer.writerows(relevant)


if __name__ == '__main__':
    load()