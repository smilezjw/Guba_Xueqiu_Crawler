# coding=utf8

from scrapy import log
from selenium import webdriver
from scrapy.http import HtmlResponse

class PhantomJSMiddleware(object):
    def process_request(self, request, spider):
        if 'PhantomJS' in request.meta:
            log.msg('PhantomJS Requesting: ' + request.url, level=log.WARNING)
            service_args = ['--load-image=false', '--disk-cache=true']
            if request.meta.has_key('proxy'):
                log.msg('PhantomJS proxy: ' + request.meta['proxy'][7:], level=log.WARNING)
                service_args.append('--proxy=' + request.meta['proxy'][7:])
            try:
                driver = webdriver.PhantomJS(executable_path='C://Zhang\ Jiawen//Anaconda//Scripts//phantomjs')
                driver.get(request.url)
                content = driver.page_source.encode('utf-8')
                # url = driver.current_url.encode('utf-8')
                driver.quit()
                if content == '<html><head></head><body></body></html>':
                    return HtmlResponse(request.url, encoding='utf-8', status=503, body=content)
                else:
                    # return HtmlResponse(request.url, encoding='utf-8', status=200, body=content)
                    return HtmlResponse(request.url)
            except Exception, e:
                log.msg('PhantomJS Exception!', level=log.WARNING)
                # return HtmlResponse(request.url, encoding='utf-8', status=503)
                return HtmlResponse(request.url)
        else:
            log.msg('Common Requesting: ' + request.url, level=log.WARNING)
