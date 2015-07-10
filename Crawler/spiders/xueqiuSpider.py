# coding=utf8

import MySQLdb
import time
import random
import json
import re
from Crawler.settings import HEADERS
from Crawler.items import XueqiuPostItem
from scrapy.spiders import Spider
from scrapy.http import FormRequest, Request
from datetime import datetime


class XueqiuSpider(Spider):
    """
    Usage: scrapy crawl XueqiuSpider -a username=13621980276 -a password=zhangjiawen1991 [--logfile=xueqiu.log]
    """
    name = "XueqiuSpider"
    allowed_domains = ["xueqiu.com"]
    start_urls = []

    def __init__(self, username, password):
        self.headers = HEADERS
        self.username = username
        self.password = password

    def start_requests(self):
        return [FormRequest(
            "http://xueqiu.com/user/login",
            formdata={'username': self.username,
                      'password': self.password,
                      },
            headers=self.headers,
            callback=self.after_login
        )]

    def after_login(self, response):
        latest_updated = self.get_latest_time()
        prefix = "http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol=%s" \
                 "&hl=0&source=all&sort=time&page=%d&_=%s"
        conn = MySQLdb.connect(host='localhost', user='root', passwd='passw0rd', db='thomas')
        cursor = conn.cursor()
        cursor.execute('select stock_id from stock limit 2')
        results = cursor.fetchall()
        for i, stockId in enumerate(results):
            stockId = stockId[0].split('.')
            stockId = stockId[1] + stockId[0]
            for page in xrange(1, 5):
                timestamp = str(int(time.time())) + str(random.randint(0, 9))
                url = prefix % (stockId, page, timestamp)
                print url
                yield Request(url, meta=latest_updated, headers=self.headers, callback=self.parse)
        cursor.close()

    def parse(self, response):
        body = json.loads(response.body)
        for post in body['list']:
            item = XueqiuPostItem()
            item['stock_id'] = re.search("(?<=symbol=)\w{2}\d{6}", response.url).group(0)
            item['stock_id'] = item['stock_id'][2:] + '.' + item['stock_id'][:2]
            item['title'] = post['title']
            item['username'] = post['user_id']
            item['content'] = post['text']
            item['created_time'] = datetime.fromtimestamp(post['created_at']/1000)
            item['comment_count'] = post['reply_count']
            item['donate_count'] = post['donate_count']
            item['forward_count'] = post['retweet_count']
            item['favourite_count'] = post['fav_count']
            if item['stock_id'] not in response.meta or item['created_time'] > response.meta[item['stock_id']]:
                yield item
            else:
                break

    def get_latest_time(self):
        latest_conn = MySQLdb.connect(host='localhost', user='root', passwd='passw0rd', db='post')
        latest_cursor = latest_conn.cursor()
        latest_cursor.execute('select stock_id, max(created_time) from xueqiu group by stock_id')
        last_updated = {}
        latest_time = latest_cursor.fetchall()
        for each in latest_time:
            last_updated[each[0]] = each[1]
        latest_cursor.close()
        return last_updated
