# coding=utf8

import re

from datetime import datetime
from scrapy.spiders import Spider
from scrapy import Selector, Request
from Crawler.items import SSEPostItem, SSEAnnouncementItem


class SSESpider(Spider):
    name = "SSE_Corporation_Announcement"
    allowed_domains = ["sse.com.cn"]
    start_urls = []

    def start_requests(self):
        url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc.htm?p=%s' \
              % (datetime.today().strftime('%a %b %d %Y %H:%M:%S') + 'GMT+0800 (China Standard Time)')
        yield self.make_requests_from_url(url)

    def parse(self, response):
        selector = Selector(response)
        for post in selector.xpath('//ul[@class="list_ul"]/li'):
            item = SSEPostItem()
            item['url'] = post.xpath('a/@href').extract()[0]
            text = post.xpath('a/text()').extract()[0].split(':')
            item['stock_id'] = text[0] + '.SH'
            item['title'] = text[1]
            item['created_time'] = post.xpath('span[@class="list_date"]/text()').extract()[0].strip('\r\n')
            filename = item['title'].strip(' *') + '.pdf'
            item['file_urls'] = [{'file_url': item['url'], 'file_name': filename}]
            yield item


class SSESpider(Spider):
    name = "SSE_Announcement_Spider"
    allowed_domains = ["sse.com.cn"]
    start_urls = ['http://www.sse.com.cn/disclosure/announcement/general/']

    def parse(self, response):
        for post in response.xpath('//ul[@class="list_ul"]/li'):
            item = SSEAnnouncementItem()
            item['url'] = 'http://www.sse.com.cn' + post.xpath('a/@href').extract()[0]
            text = post.xpath('a/text()').extract()[0]
            stock_id = re.search(u'\uff08\d+\uff09', text)
            if stock_id is not None:
                item['stock_id'] = stock_id.group()[1:-1] + '.SH'
            else:
                item['stock_id'] = None
            item['title'] = text
            item['created_time'] = post.xpath('span[@class="list_date"]/text()').extract()[0]
            yield Request(url=item['url'], meta={'item': item}, callback=self.parse_announcement)

    def parse_announcement(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//div[@class="block_l1"]').extract()
        yield item
