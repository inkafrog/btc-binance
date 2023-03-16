import os

class Helper:

    def calculateQuantity(maxBtc, askPrice):
        return float(maxBtc) / float(askPrice)

    def getUsername():
        print('Please Enter Username:')
        ask = input('>>| ')
        return ask

    def check(file):
        if not os.path.exists(file):
            exit('Sorry User is not exists!')

    def delete(file):
        try:
            os.remove(file)
        except FileNotFoundError:
            exit("Sorry File is not exists!")

    def addExt(user):
        return user + '.cfg'

    def isRedir(res):
        if res.ok:
            if len(res.history) > 1:
                return not 'login' in res.history[-1].url.lower()
            elif len(res.history) == 1:
                return not 'login' in res.history[0].url.lower()
            else:
                return True

        else:
            return False
