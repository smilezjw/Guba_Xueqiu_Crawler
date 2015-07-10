# coding=utf8


import urllib, urllib2
import time
from random import randint
import cookielib

def xueqiu():
    # 设置cookie
    CookieJar = cookielib.CookieJar()
    CookieProcessor = urllib2.HTTPCookieProcessor(CookieJar)
    opener = urllib2.build_opener(CookieProcessor)
    urllib2.install_opener(opener)

    # 登陆获得cookie
    params = urllib.urlencode({'username': 'xxxxxxxx', 'password':'xxxxxxxx'}).encode('UTF8')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}
    req = urllib2.Request('http://xueqiu.com/user/login', params, headers=headers)
    httpf = opener.open(req, params)

    # 获取内容
    url = 'http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol=SZ000001&hl=0&source=all&' \
          'sort=alpha&page=1&_=1435819638168'
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read().decode('utf-8')
    ff = open('xueqiu.json', 'w+')
    print >>ff, content.encode('utf8')


if __name__ == '__main__':
    xueqiu()
