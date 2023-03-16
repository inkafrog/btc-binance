import requests
import re

from bs4 import BeautifulSoup as bs

from .exception import *
from .helper import Helper

class Web:

    def doLogin(user, passwd):
        cookies = {
            'cookie: __cfduid': 'd6cbe8c0e0d07b0810c3c33f3f582f2e01519480257',
            'PHPSESSID': 'v7he7u49q9h3gvvq5bj3v9cvq5',
            '_ga': 'GA1.2.730273978.1519480279',
            'seerid': '8a5a7e227a3b6b62e566997968b656b0',
            '_gid': 'GA1.2.309880369.1520474305',
            'wordpress_test_cookie': 'WP+Cookie+check',
            'seerses': 'e',
            'ly_segs': '%7B%22all1%22%3A%22all1%22%2C%22palm_beach_research_group_master%22%3A%22palm_beach_research_group_master%22%2C%22ly_unknown_email%22%3A%22ly_unknown_email%22%2C%22ly_frequent_user%22%3A%22ly_frequent_user%22%2C%22smt_power%22%3A%22smt_power%22%2C%22all%22%3A%22all%22%7D',
            'AWSALB': 'XZ6jBKhahUlB6OMOqYTQvDu25eNRYfpppj3WVRLr5hUUGKmFPNVCEtqzfJIjRYaDfXGG3UliALy/kCJfA76oqSxJr60HxHUBv1HxczZgWn4hQFUT1jjQTxWNvbcY',
            'PathforaPageView': '16',
        }

        headers = {
            'origin': 'https://www.palmbeachgroup.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'pragma': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cache-control': 'no-cache',
            'authority': 'www.palmbeachgroup.com',
            'referer': 'https://www.palmbeachgroup.com/login/',
        }

        data = [
          ('log', user),
          ('pwd', passwd),
          ('rememberme', 'forever'),
          ('redirect_to', 'https://www.palmbeachgroup.com'),
        ]

        session = requests.Session()

        response = session.post('https://www.palmbeachgroup.com/wp-login.php', headers=headers, cookies=cookies, data=data)

        if not Helper.isRedir(response):
            raise LoginFailed("Cannot Able to Login")
        else:
            return session

    def getAlertLinks(session, anchorText = 'buy alert', url = "https://www.palmbeachgroup.com/updates/?filter=pbo"):
        req = session.get(url)

        if Helper.isRedir(req):
            b = bs(req.text, "html.parser")
            posts = b.find_all("div", {"class": "post-entry-stack"})
            links = []
            for post in posts:
                post = post.find("h2", {"class": "entry-title"}).find("a")
                if 'buy alert' in post.text.lower():
                    links.append(post.get('href'))
                    break

            return set(links)
        else:
            raise SessionExpired('Session Expired While Scrapping Links')

    def getMonthlyLinks(session, url = 'https://www.palmbeachgroup.com/monthly-issues/?filter=pbo'):
        req = session.get(url)

        if Helper.isRedir(req):
            b = bs(req.text, "html.parser")
            links = b.find("div", {"class": "post-entry-stack"}).find("h2", {"class": "entry-title"}).find("a").get("href")

            return [links]
        else:
            raise SessionExpired('Session Expired While Scrapping Links')


    def getCoin(session, link, regex=r'Buy.*?\((.*?)\)'):
        req = session.get(link)

        if Helper.isRedir(req):
            content = req.text
            find = re.findall(regex, content)

            if find:
                return find[0]
            else:
                raise ParseError('Cannot Able to Parse Coin From Link: '.format(link))

        else:
            raise SessionExpired('Session Expired While Scrapping Coin From: {}'.format(link))
