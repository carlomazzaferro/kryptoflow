from gdax import AuthenticatedClient
from kryptoflow.managers.secrets import SecretsManager


class Trader(object):

    def __init__(self, market='BTC-USD', live=True):
        self.product = market
        if live:
            url = "https://api.gdax.com"
        else:
            url = "https://api-public.sandbox.gdax.com"
        self.auth_client = AuthenticatedClient(*SecretsManager.get_value('gdax'), api_url=url)

    @property
    def is_authenticated(self):
        try:
            return self.auth_client.get_accounts()
        except Exception as e:
            print(e, 'Failed to retrieve account information')

    def post_buy(self, price, size):
        self.auth_client.buy(price=str(price),  # USD
                             size=str(size),  # BTC
                             product_id=self.product)

    def post_sell(self, price, size):
        self.auth_client.sell(price=str(price),  # USD
                              size=str(size),  # BTC
                              product_id=self.product)



