import binance
from Module.web import Web
from Module.config import Config
from Module.helper import Helper
from Module.binance import Binance
from Module.style import print
from Module.db import Database
from time import sleep
from notifypy.notify import Notify
from time import sleep
from retrying import retry

class Caller(object):
    def __init__(self, username):
        self.username = username
        config = Config()
        self.config = config.readUser(username)

        APIKEY = self.config.get('binance', 'apikey')
        APISECRET = self.config.get('binance', 'apisecret')

        # binance
        self.binance = Binance(APIKEY, APISECRET)

        # database
        self.db = Database()

        # gmail
        self.guser = self.config.get('Notification', 'Username')
        self.gpassword = self.config.get('Notification', 'Password')
        # notification receiver
        self.receiver = self.config.get('Notification', 'Email')

        # ...
        self.notify = Notify(self.guser, self.gpassword, 'gmail')

    @retry(wait_fixed=3000, stop_max_attempt_number=30)
    def updateChecker(self):
        user = self.config.get('Website', 'Username')
        password = self.config.get('Website', 'Password')

        print('Logging Into Website')
        session = Web.doLogin(user, password)

        print('Parsing Alert Links')
        links = Web.getAlertLinks(session)

        print('Total Links:', len(links))

        for link in links:

            print('Parsing Coin From Alert Link:', link)

            coin = Web.getCoin(session, link)

            if coin.lower() == 'btc':
                continue

            print(coin, 'Found!')

            # check if already done
            if self.db.checkIsDone(self.username,  coin) or self.db.checkIsInQueue(self.username, coin):
                print('Already Done or Is In Queue')
                continue

            print('Getting Ticker Price')
            ticker = self.binance.getTicker(coin)

            if ticker is None:
                print('Seems like this coin is not available on binance!')
                continue

            price = ticker['askPrice']
            # percentage
            percentage = ticker['priceChangePercent']

            # our user BTC
            btc = self.config.getfloat('Trade', 'btc')

            # calculateQuantity
            quantity = Helper.calculateQuantity(btc, price)

            print('Going to Buy', coin, 'coin', 'Calculate Quantity is:', quantity,  btc, 'BTC')

            # place order
            order = self.binance.buyCoin(coin, quantity)

            print(order)

            if order:
                # now insert into database
                print("Coin Trade Placed Successfully!")

                self.db.insertIntoQueue(self.username, coin)

    # @retry(wait_fixed=3000, stop_max_attempt_number=30)
    def issueChecker(self):
        user = self.config.get('Website', 'Username')
        password = self.config.get('Website', 'Password')

        print('Logging Into Website')
        session = Web.doLogin(user, password)

        print('Parsing Monthly Links')
        links = Web.getMonthlyLinks(session)

        print('Total Links:', len(links))

        for link in links:
            coin = Web.getCoin(session, link)

            if coin.lower() == 'btc':
                continue

            # Now buy coin etc
            print(coin, 'Found!')

            # check if already done
            if self.db.checkIsDone(self.username,  coin) or self.db.checkIsInQueue(self.username, coin):
                print('Already Done or Is In Queue')
                continue

            print('Getting Ticker Price')
            ticker = self.binance.getTicker(coin)

            if ticker is None:
                print('Seems like this coin is not available on binance!')
                continue

            price = ticker['askPrice']
            # percentage
            percentage = ticker['priceChangePercent']

            # our user BTC
            btc = self.config.getfloat('Trade', 'btc')

            # calculateQuantity
            quantity = Helper.calculateQuantity(btc, price)

            print('Going to Buy', coin, 'coin', 'Calculate Quantity is:', quantity,  btc, 'BTC')

            # try:
            #     # place order
            order = self.binance.buyCoin(coin, quantity)
            # except Exception as e:
            #     statusCode = e.code
            #
            #     if statusCode == -2010:
            #         title = 'InsufficentBalance For Buying: "{}" In User: "{}"'.format(coin, self.username)
            #         print(title)
            #         if not self.db.isNotiSend(self.username, coin, 'InsufficentBalance'):
            #             self.notify.sendNotification(title, '<pre>{}</pre><br />This Message Will not send again! if occur in same coin'.format(e))
            #
            #         continue
            #     else:
            #         raise e

            if order:
                print(order)
                # now insert into database
                print("Coin Trade Placed Successfully!")

                self.db.insertIntoQueue(self.username, coin)

    @retry(wait_fixed=3000, stop_max_attempt_number=30)
    def tradeWatcher(self):
        # get all coins from trade
        coins = self.db.getQueueSymbols(self.username)

        for coin in coins:
            coin = coin['symbol']
            ticker = self.binance.getTicker(coin)

            # percentage
            percentage = float(ticker['priceChangePercent'])
            myPercentage = self.config.getfloat('Trade', 'percentage')

            if percentage >= myPercentage:
                # sell
                print('Selling {}'.format(coin))
                # self.binance.sellCoin(coin)
                # send notification

                title = '"{}" Coin Is Sell Successfully'.format(coin)
                message = '''This is an automate message from BTC Binace Bot To notify that "{}" Coin is
                Sell Successfully On percentage: "{}"
                '''.format(coin, percentage)
                self.notify.sendNotification(self.receiver, title, message)
                # removeFromQueue
                self.db.removeFromQueue(self.username, coin)

                print(title)
