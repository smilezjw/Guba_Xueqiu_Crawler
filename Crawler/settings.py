# -*- coding: utf-8 -*-

# Scrapy settings for Crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Crawler'

SPIDER_MODULES = ['Crawler.spiders']
NEWSPIDER_MODULE = 'Crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Crawler (+http://www.yourdomain.com)'

# lower value, higher priority
ITEM_PIPELINES = {'Crawler.pipelines.PostPipeline': 100,
                  'Crawler.pipelines.GubaPostPipeline': 300,
                  'Crawler.pipelines.XueqiuPostPipeline': 300,
                  'Crawler.pipelines.SSEPostPipeline': 300,
                  'Crawler.pipelines.SSEAnnouncementPostPipeline': 300,
                  'Crawler.pipelines.SSEPdfPipeline': 200,
                  }
FILES_STORE = '/Zhang Jiawen/Crawler/SSE_pdf'

DOWNLOAD_DELAY = 1.0    # 1s of delay

# # Enables scheduling storing requests queue in redis.
# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
#
# # Don't cleanup redis queue, allows to pause/resume crawls.
# SCHEDULER_PERSIST = True
#
# # Schedule requests using a priority queue. (default)
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
#
# # Schedule requests using a queue (FIFO)
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
#
# # Schedule requests using a stack (LIFO).
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'
#
# # Max idle time to prevent the spider from being closed when distributed crawling.
# # This only works if queue class is SpiderQueue or SpiderStack,
# # and may also block the same time when your spider start at the first time (because the queue is empty).
# SCHEDULER_IDLE_BEFORE_CLOSE = 10#
#
# # Specify the host and port to use when connecting to Redis
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
# REDIS_URL = 'redis://user:pass@hostname:9001'

# DOWNLOADER_MIDDLEWARES = {
#     'Crawler.middlewares.PhantomJSMiddleware': 1000
# }

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
}



