from binance.client import Client
from Module.style import print
from Module.exception import *
import binance

class Binance:

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

        self.client = None

    def init(self):
        if self.client is None:
            self.client = Client(self.key, self.secret)


    def setSymbol(self, symbol):
        symbol =  symbol + 'BTC'

        self.init()

        return symbol

    def getTicker(self, symbol):
        symbol = self.setSymbol(symbol)

        try:
            ticker = self.client.get_ticker(symbol=symbol)
        except binance.exceptions.BinanceAPIException as e:
            statusCode = e.code
            if statusCode == -1121:
                return None
            else:
                raise UnkownBinanceError(e)

        return ticker

    def buyCoin(self, symbol, quantity):
        symbol = self.setSymbol(symbol)


        minQty = self.getMinimumQantity(symbol)
        # now let's calculateQuantity
        print(quantity, minQty)
        print(quantity >= minQty)
        print(symbol)
        if not quantity >= minQty:
            print('Quantity is not greater than or equal to minimum quantity')
            print('adjusting to minimum Quantity:', minQty)
            quantity = minQty

        ischecked = None

        while 1:
            try:
                # now place
                order = self.client.create_order(
                    symbol = symbol,
                    side = Client.SIDE_BUY,
                    type = Client.ORDER_TYPE_MARKET,
                    quantity = quantity
                )
                break
            except binance.exceptions.BinanceAPIException as e:
                statusCode = e.code
                if statusCode == -2010:
                    # send notification
                    # raise InsufficentBalance('InsufficentBalance For Buying "{}"'.format(symbol))
                    return None
                elif statusCode == -1013 and ischecked is None:
                    # convert quantity to int
                    quantity = int(quantity)
                    ischecked = True
                else:
                    raise UnkownBinanceError(e)


        return order

    def getBalances(self):
        account = self.client.get_account()
        balances = account['balances']

        return balances

    def getBalance(self, coin):
        balances = self.getBalances()
        for balance in balances:
            asset = balance['asset'].lower()
            coin = coin.lower()

            if coin == asset:
                return float(balance['free'])

    def getMinimumQantity(self, symbol):
        return float(self.client.get_symbol_info(symbol=symbol)['filters'][1]['minQty'])

    def sellCoin(self, symbol):
        # symbol == coin and search for it
        quantity = self.getBalance(symbol)

        # becareful here
        if not quantity > 0:
            return

        symbol = self.setSymbol(symbol)

        # now place
        order = self.client.create_order(
            symbol = symbol,
            side = Client.SIDE_SELL,
            type = Client.ORDER_TYPE_MARKET,
            quantity = quantity
        )


        return order
