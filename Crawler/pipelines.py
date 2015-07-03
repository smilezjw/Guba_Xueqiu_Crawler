# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi
from scrapy import log


class PostPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host='127.0.0.1',
                                            db='post',
                                            user='root',
                                            passwd='passw0rd',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True
                                            )


class GubaPostPipeline(PostPipeline):
    def process_item(self, item, spider):
        if spider.name != "GubaSpider":
            return item
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

    def _conditional_insert(self, tx, item):
        tx.execute(
            'insert into guba (stock_id, url, title, username, content, created_time, updated_time, '
            '                  read_count, comment_count)'
            + 'values         (%s,       %s,  %s,    %s,       %s,      %s,           %s,'
              '                %s,            %s)',
            (item['stock_id'],
             item['url'],
             ''.join(item['title']),
             ''.join(item['username']),
             ''.join(item['content']),
             item['created_time'],
             item['updated_time'],
             item['read_count'],
             item['comment_count'],
             #item['thumbup_count'],
             # item['forward_count'][0],
             # item['share_count'][0],
             # item['favourite_count'][0]
             )
        )

    def handle_error(self, e):
        log.err(e)


class XueqiuPostPipeline(PostPipeline):
    def process_item(self, item, spider):
        if spider.name != "XueqiuSpider":
            return item
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

    def _conditional_insert(self, tx, item):
        tx.execute(
            'insert into xueqiu (stock_id, title, username, content, created_time,'
            '                    comment_count, donate_count, forward_count, favourite_count)'
            + 'values           (%s,       %s,    %s,       %s,      %s,'
              '                  %s,              %s,          %s,            %s)',
            (item['stock_id'],
             item['title'],
             item['username'],
             item['content'],
             item['created_time'],
             # item['updated_time'],
             item['comment_count'],
             item['donate_count'],
             item['forward_count'],
             item['favourite_count']
             )
        )

    def handle_error(self, e):
        log.err(e)

