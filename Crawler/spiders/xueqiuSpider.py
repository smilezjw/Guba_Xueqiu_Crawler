# coding=utf8

import MySQLdb
import time
import random
import json
import re
from Crawler.settings import HEADERS, COOKIES
from Crawler.items import XueqiuPostItem
from scrapy.spider import Spider
from scrapy.http import FormRequest
from datetime import datetime


class XueqiuSpider(Spider):
    name = "XueqiuSpider"
    allowed_domains = ["xueqiu.com"]
    start_urls = []

    def __init__(self):
        self.headers = HEADERS
        self.cookies = COOKIES

    def start_requests(self):
        prefix = "http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol=%s" \
                 "&hl=0&source=all&sort=alpha&page=%d&_=%s"
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
                yield FormRequest(url, meta={'cookiejar': i}, headers=self.headers,
                                  cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        body = json.loads(response.body)
        for post in body['list']:
            item = XueqiuPostItem()
            item['stock_id'] = re.search("(?<=symbol=)\w{2}\d{6}", response.url).group(0)
            item['stock_id'] = item['stock_id'][2:] + '.' + item['stock_id'][:2]
            item['title'] = post['title']
            item['username'] = post['user_id']
            item['content'] = post['text']
            item['created_time'] = datetime.utcfromtimestamp(long(str(post['created_at'])[:-3]))
            item['comment_count'] = post['reply_count']
            item['donate_count'] = post['donate_count']
            item['forward_count'] = post['retweet_count']
            item['favourite_count'] = post['fav_count']
            yield item
