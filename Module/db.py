import dataset

class Database:

    def __init__(self):
        self.db = dataset.connect('sqlite:///database.db', check_same_thread=False)

    def getQueueSymbols(self, username):
        table = self.db['symbol']

        return table.find(username=username)


    def checkIsInQueue(self, username, symbol):
        table = self.db['symbol']

        chk = table.find(symbol=symbol, username=username)

        if sum(1 for k in chk) <= 0:
            return None

        return chk

    def checkIsDone(self, username, symbol):
        table = self.db['doneSymbol']

        chk = table.find(symbol=symbol, username=username)

        if sum(1 for k in chk) <= 0:
            return None

        return chk

    def insertIntoQueue(self, username, symbol):
        if self.checkIsInQueue(username, symbol):
            return

        table = self.db['symbol']

        data = {
            'symbol': symbol,
            'username': username,
        }

        table.insert(data)

    def insertIntoDone(self, username, symbol):
        table = self.db['doneSymbol']

        return table.insert(dict(symbol=symbol, username=username))

    def isNotiSend(self, username, symbol, type):
        table = self.db['error_noti']

        data = {
            'username': username,
            'symbol': symbol,
            'type': type,
        }

        # first check if not already exists then insert
        chk = table.find(data)

        if sum(1 for k in chk) <= 0:
            table.insert(data)

            return False

        return True

    def removeFromQueue(self, username, symbol):
        table = self.db['symbol']

        table.delete(username=username, symbol=symbol)

        # now insert into checkIsDone
        self.insertIntoDone(username, symbol)
