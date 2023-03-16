from configparser import RawConfigParser
from .style import *
from .helper import Helper

class Config:

    def __init__(self):
        pass

    def createUser(self):
        # config file name
        print('Please Enter Username:')
        user = input('>>| ')

        # config object
        config = RawConfigParser()

        config.add_section('Website')
        # Website login details
        print('Please Enter Website Login Details')
        print('Email:')
        email = input('>>| ')
        config.set('Website', 'Username', email)

        # password
        print('Password:')
        password = input('>>| ')
        config.set('Website', 'Password', password)

        # now other config details
        # let give this section name Trade
        config.add_section('Trade')
        print('Please Enter Amount of BTC for each Trade:')
        btcAmount = input('>>| ')
        config.set('Trade', 'Btc', btcAmount)

        # %
        print('Please Enter Percentage for selling Trade of each coin:')
        percentage = input('>>| ')
        config.set('Trade', 'Percentage', percentage)

        # API
        # Binance
        config.add_section('binance')
        print('Please Enter Binance API:')

        print('API Key')
        binanceKey = input('>>| ')
        config.set('binance', 'APIkey', binanceKey)

        print('API Secret')
        binanceSecret = input('>>| ')
        config.set('binance', 'APIsecret', binanceSecret)

        # create another section config
        config.add_section('Timer')
        print('Please Enter Timer Configuration Details:')

        print('Please Enter "Updates" Page Timer in seconds:')
        updatesTimer = input('>>| ')
        config.set('Timer', 'UpdatePages', updatesTimer)


        print('Please Enter "Issue" Page Timer in seconds:')
        issueTimer = input('>>| ')
        config.set('Timer', 'IssuePages', issueTimer)

        # create another section config
        config.add_section('Notification')
        print('Please Enter Notification Email Details:')

        print('Please Enter Gmail "Username":')
        guser = input('>>| ')
        config.set('Notification', 'Username', guser)

        print('Please Enter Gmail "Password":')
        password = input('>>| ')
        config.set('Notification', 'Password', password)


        print('Please Enter Email Addresses Who will receive notifications (seprated by comma ",")')
        addresses = input('>>| ')
        config.set('Notification', 'Email', addresses)

        file = Helper.addExt(user)
        with open(file, 'w') as out:
            config.write(out)

    def readUser(self, username):
        file = Helper.addExt(username)

        Helper.check(file)

        config = RawConfigParser()
        config.read(
            file
        )

        return config

    def modifyUser(self, username):
        config = self.readUser(username)

        # now look for changes
        i = 1
        sections = []
        for section in config._sections:
            print('{}. {}'.format(i, section))
            sections.append(section)
            i += 1

        while 1:
            print('Please Enter Which Section you want to edit?')
            ask = int(input('>>| ')) - 1
            if len(config._sections) > ask:
                sectionName = sections[ask]
                break
        # get section values
        section = config._sections[sectionName]

        # now print parts
        values = []
        i = 1
        for value in section:
            print('{}. {}'.format(i, value))
            values.append(value)

            i += 1

        while 1:
            print('Please Select Which Part You want edit Of Section: {}'.format(sectionName))
            ask = int(input('>>| ')) - 1
            if len(config._sections) > ask:
                value = values[ask]
                break

        print('Please Enter New Value Of "{}"'.format(value))
        ask = input('>>| ')
        section[value] = ask


        file = Helper.addExt(username)
        # now write back
        with open(file, 'w') as out:
            config.write(out)

        print('Edit Successfully!')

    def displayUser(self, username):
        config = self.readUser(username)

        # now look for changes
        i = 1
        sections = []
        for section in config._sections:
            print('{}. {}'.format(i, section))
            sections.append(section)
            i += 1

        while 1:
            print('Please Enter Which Section Data you want to see?')
            ask = int(input('>>| ')) - 1
            if len(config._sections) > ask:
                sectionName = sections[ask]
                break
        # get section values
        section = config._sections[sectionName]

        print('Data For Section:', sectionName)
        for data in section:
            print(data + ':', section[data])

    def deleteUser(self, username):
        file = Helper.addExt(username)

        Helper.check(file)

        Helper.delete(file)
