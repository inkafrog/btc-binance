from Module.helper import Helper
from Module.caller import Caller
from Module.config import Config
from Module.logger import Logger
from Module.style import *
from time import sleep
from threading import Thread
from queue import Queue
from notifypy.decorator import PyNoti

username = Helper.getUsername()
config = Config()
config = config.readUser(username)

log = Logger()
logger = log.create('error', 'error.log')

class Main(object):

    @PyNoti(config.get('Notification', 'Username'), config.get('Notification', 'Password'), config.get('Notification', 'Email'), logger=logger)
    def runIssueCheck(self, user, q):
        while 1:
            call = Caller(user)
            call.issueChecker()

            config = Config()
            config = config.readUser(user)

            # get timers
            timer = config.getfloat('Timer','issuepages')

            print('Going To wait {} Seconds for next round'.format(timer))
            sleep(timer)

        q.task_done()

    @PyNoti(config.get('Notification', 'Username'), config.get('Notification', 'Password'), config.get('Notification', 'Email'), logger=logger)
    def runUpdateCheck(self, user, q):
        while 1:
            print('Running Update Page checker')
            call = Caller(user)
            call.updateChecker()

            config = Config()
            config = config.readUser(user)

            timer = config.getfloat('Timer','updatepages')

            # get timers
            print('Going To wait {} Seconds for next round'.format(timer))
            sleep(timer)

        q.task_done()

    @PyNoti(config.get('Notification', 'Username'), config.get('Notification', 'Password'), config.get('Notification', 'Email'), logger=logger)
    def runTradeCheck(self, user, q):
        while True:
            call = Caller(user)
            call.tradeWatcher()

            sleep(1)
        q.task_done()

if __name__ == '__main__':
    main = Main()
    q = Queue()

    # Trade Watcher
    q.put('trade')
    worker = Thread(target=main.runTradeCheck, args=(username, q))
    worker.setDaemon(True)
    worker.start()

    # Update Page Thread
    q.put('update')
    worker = Thread(target=main.runUpdateCheck, args=(username, q))
    worker.setDaemon(True)
    worker.start()

    sleep(10)

    # Issue Page thread
    q.put('issue')
    worker = Thread(target=main.runIssueCheck, args=(username, q))
    worker.setDaemon(True)
    worker.start()

    q.join()
