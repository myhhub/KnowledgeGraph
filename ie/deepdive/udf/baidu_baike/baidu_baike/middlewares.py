# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

class WeixinSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgent:
    def __init__(self, agents):
        self.agents =[
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media      Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.   30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
            ]        
                     
    @classmethod     
    def from_crawler(cls,crawler):
        # 获取settings的USER_AGENT列表并返回
        return cls(crawler.settings.getlist('USER_AGENTS'))
    def process_request(self, request, spider):
        # 随机设置Request报头header的User-Agent
        request.headers.setdefault('User-Agent', random.choice(self.agents))
                     
# 添加代理           
                     
class ProxyMiddleWare(object):
    proxy_list=[     
   "http://58.87.89.234:3128",
    "http://139.201.202.140:53281",
    "http://27.37.123.30:9000",
    "http://218.67.82.146:36709",
    "http://222.222.169.60:53281",
    "http://120.33.247.233:46884",
    "http://114.215.18.7:3128",
    "http://112.74.94.142:3128",
    "http://122.72.18.34:80",
    "http://36.33.25.123:808",
    "http://123.138.89.133:9999",
    "http://111.231.192.61:8080",
    "http://59.41.202.228:53281",
    "http://222.241.14.187:8888",
    "http://61.155.164.106:3128",
    "http://27.40.156.43:61234",
    "http://14.29.84.50:8080",
    "http://116.25.100.62:9797",
    "http://58.21.183.144:80",
    "http://14.221.166.205:9000",
    "http://115.231.50.10:53281",
    "http://120.34.205.40:808",
    "http://123.139.56.238:9999",
    "http://113.116.170.232:9000",
    "http://116.17.236.36:808",
    "http://114.232.163.73:34837",
    "http://171.35.103.37:808",
    "http://27.46.51.232:9797",
    "http://223.247.255.207:24714",
    "http://223.241.117.179:8010",
    "http://222.186.12.102:57624"]

def process_request(self,request,spider):
    # if not request.meta['proxies']:
    ip = random.choice(self.proxy_list)
    request.meta['proxy'] = ip 

