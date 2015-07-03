# coding=utf8

import re
import MySQLdb
from scrapy.spider import Spider
from scrapy import Selector, log
from scrapy.http import Request
from Crawler.items import GubaPostItem
# from Crawler.spiders.startURLs import GetStartURLs
# from scrapy_redis.spiders import RedisSpider


class GubaSpider(Spider):
    name = "GubaSpider"
    allowed_domains = ["guba.eastmoney.com"]
    start_urls = ['http://guba.eastmoney.com/list,000001.html']

    # get start_urls from database stock_id
    def start_requests(self):
        stock_id = []
        conn = MySQLdb.connect(host='localhost', user='root', passwd='passw0rd', db='thomas')
        cursor = conn.cursor()
        cursor.execute('select stock_id from stock limit 1')
        results = cursor.fetchall()
        for stockId in results:
            stock_id.append(stockId[0][:6])
        prefix = "http://guba.eastmoney.com/list,"
        for stock_id in stock_id:
            url = prefix + str(stock_id) + ".html"
            yield self.make_requests_from_url(url)

    def parse(self, response):
        selector = Selector(response)
        posts = selector.xpath('//div[@class="articleh"]') + selector.xpath('//div[@class="articleh odd"]')
        for index, post in enumerate(posts):
            item = GubaPostItem()
            item['stock_id'] = re.search('\d+', response.url).group(0)
            item['read_count'] = int(post.xpath('span[@class="l1"]/text()').extract()[0])
            item['comment_count'] = int(post.xpath('span[@class="l2"]/text()').extract()[0])
            item['username'] = post.xpath('span[@class="l4"]/text()').extract()
            item['updated_time'] = post.xpath('span[@class="l5"]/text()').extract()[0]
            link = post.xpath('span[@class="l3"]/a/@href').extract()
            print item['updated_time']
            if link:
                if link[0].startswith('/'):
                    link = "http://guba.eastmoney.com/" + link[0][1:]
                else:
                    link = "http://guba.eastmoney.com/" + link[0]
                item['url'] = link
                yield Request(url=link, meta={'item': item, 'PhantomJS': True}, callback=self.parse_post)
        for pagenum in xrange(2, 5):
            url = response.url.split('_')
            if len(url) == 1:
                nextpage = url[0][:-5] + '_' + str(pagenum) + '.html'
            elif len(url) == 2:
                nextpage = url[0] + '_' + str(pagenum) + '.html'
            else:
                break
            yield Request(url=nextpage, callback=self.parse)

    def parse_post(self, response):
        item = response.meta['item']
        selector = Selector(response)
        item['title'] = selector.xpath('//div[@id="zwconttbt"]/text()').extract()
        item['created_time'] = re.search('[\d\-: ]+', selector.xpath('//div[@class="zwfbtime"]/text()').extract()[0]).group(0)
        item['content'] = selector.xpath('//div[@id="zwconbody"]').extract()
        item['updated_time'] = item['created_time'][1:5] + '-' + item['updated_time']
        print item['updated_time']
        yield item
        # item['thumbup_count'] = selector.xpath('//div[@class="zwconbtnsi"]/span[@id="zwpraise"]/a/span/text()').extract()
        # updated_link = selector.xpath('//div[@id="zwcontabsort"]/a/@href').extract()
        # if len(updated_link) == 3:
        #     updated_link = "http://guba.eastmoney.com/" + updated_link[1]
        #     yield Request(url=updated_link, meta={'item': item}, callback=self.parse_updated_time)
        # else:
        #     item["updated_time"] = None
        #     yield item

    # def parse_updated_time(self, response):
    #     item = response.meta['item']
    #     selector = Selector(response)
    #     item['updated_time'] = re.search('\d+[\d\-: ]+',
    #                                      selector.xpath('//div[@id="zwlist"]/div[@class="zwli clearfix"]'
    #                                                     '/div[@class="zwlitx"]/div/div[@class="zwlitime"]/text()').extract()[0]).group(0)
    #     return item
