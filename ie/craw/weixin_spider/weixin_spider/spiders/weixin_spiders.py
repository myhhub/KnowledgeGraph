#!/usr/bin/env python
# coding=utf-8

from weixin_spider.items import WeixinSpiderItem
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import copy
#from scrapy.spider import BaseSpider
import json
import re
import time

class WeixinSpider(scrapy.Spider):
    name = 'weixin'
#    allowed_domains = ['weixin.sougou.com']
    headers = {
        'Host': 'weixin.sougou.com',
        'Referer': 'http://weixin.sogou.com/weixin? type=2&s_from=input&query=%E6%B5%85%E5%B1%B1%E5%B0%8F%E7%AD%91&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=5109&sst0=1513697178371&lkt=0%2C0%2C0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    print "参数1：按公众号名称搜索；参数2：按关键字进行搜索"
    choice = input("请输入查询模式: ")
    page = 1
    init_auth = set()

    def start_requests(self):
        if self.choice == 1:
            id = raw_input("请输入你要查询的公众号id: ")
#            id = 'almosthuman2014'  # 默认机器之心公众号，使用时请去除
            id = 'shenzhengig'
            start_urls = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=' + str(id) + '&ie=utf8&_sug_=n&_sug_type_='
            return [Request(start_urls, callback=self.parse)]

        elif self.choice == 2:
            key = raw_input("请输入要查询的关键字： ")
            maxNo = int( input("请输入查询的最大页码： ") )
            return [scrapy.FormRequest(
                url='http://weixin.sogou.com/weixin',
                formdata={
                    'type': '2',
                    'ie': 'utf8',
                    'query': key,
                    'tsn': '1',
                    'ft': '',
                    'et': '',
                    'interation': '',
                    'sst0': str(int(time.time()*1000)),
                    'page': str(self.page),
                    'wxid': '',
                    'usip': ''
                },
                method='get',
                meta={'key':key, 'maxNo':maxNo},
                headers=self.headers,
                callback=self.parse2
                )]
        else:
            print "请输入 1 或者2 进行选择"
            return

    def parse(self, response):
        # 获取公众号URL
        publicUrl = response.xpath("//p[@class='tit']/a[@target='_blank']/@href").extract()[0]
        print("*********"+publicUrl+"************")  
        yield scrapy.Request(publicUrl,cookies={'viewed':'"1083428"', '__utmv':'30149280.3975'}, callback = self.parseArticleList)

    def parseArticleList(self, response):
        print "OK? "
        patt = re.compile(r'var msgList = (\{.*?\});')
        result = patt.search(response.text)
        url_list = json.loads(result.group(1))['list']
        for i, data in enumerate(url_list):
                title = data['app_msg_ext_info']['title']
                article_url = data['app_msg_ext_info']['content_url']
                url = 'https://mp.weixin.qq.com' + article_url.replace(r'amp;', '')
                juge_down = i
                yield scrapy.Request(url,meta={'title':title, 'juge_down': juge_down}, callback=self.parseArticle)
                           
    def parseArticle(self, response):         
            item = WeixinSpiderItem()        
            item['title'] = response.meta['title'].strip().replace(' ', '')
            juge_down = response.meta['juge_down']
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                item['publishTime'] = soup.find('em',attrs={'class':'rich_media_meta rich_media_meta_text'}).get_text().strip().replace(' ', '')
            except:
                item['publishTime'] = None
            item['article'] = soup.find('div', attrs={'class': 'rich_media_content '}).get_text()
            item['publicName'] = response.xpath('//span[@id="profileBt"]/a/text()').extract()[0].strip().replace(' ', '')
            try:
                item['cite'] = response.xpath('//span[@class="rich_media_meta rich_media_meta_text"]/text()').extract()[0]
            except:
                item['cite'] = item['publicName']
            if item['cite'] != item['publicName']:
                print u"非首发文章，新添公众号 ", item['cite'].strip().replace(' ', '')
                self.init_auth.add(item['cite'].strip().replace(' ', ''))
            yield item

            print "init_auth: ", self.init_auth, "juge_down: ", juge_down
            if juge_down == 0 and len(self.init_auth) != 0:
                tmp_auth = copy.deepcopy(self.init_auth)
                for auth in tmp_auth:
                    print "auth: ", auth
                    cite_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=' + str(auth) + '&ie=utf8&_sug_=n&_sug_type_='
                    self.init_auth.remove(auth)
                    yield scrapy.Request(cite_url, meta={'item': auth}, callback=self.parsePublicName )

    def parsePublicName(self, response):
        item = response.meta['item']
        account_name = response.xpath('//a[re:test(@uigs, "account_name_.")]/em/text()').extract()
        print "account_name: ", account_name, "###############", item
        auigs = ''
        for i, name in enumerate(account_name):
            if item == name:
                auigs = "account_name_" + str(i)
        path = '//a[@uigs=' + auigs + ']/@href'
        try:
            print "前往原创公众号： ", item
            account_url = response.xpath(('//a[@uigs="%s"]/@href') % (auigs)).extract()[0]
            request =  scrapy.Request(account_url, callback=self.parseArticleList)
            request.meta['account_url'] = account_url
            yield request
        except:
            print ": 该公众号不存在。" 
            pass 

    def parse_newPublic(self, response):
        account_url = response.meta['account_url']
        yield scrapy.Request(account_url, callback=self.parseArticleList1)
    
    def parse2(self, response):
            key = response.meta['key']
            maxNo = response.meta['maxNo']
            soup = BeautifulSoup(response.text, 'lxml')
            node_soup = soup.find('ul', attrs={'class': 'news-list'})
            
            for node in node_soup.findAll('li'):
                    url = node.select('div h3 a')[0]['href']
                    yield scrapy.Request(url, callback=self.parseArticleBody)
            
            # 实现翻页爬取
            while self.page < maxNo:
                            self.page += 1
                            yield scrapy.FormRequest(url='http://weixin.sogou.com/weixin',
                                    formdata={'type': '2','ie': 'utf8','query': key,'tsn': '1','ft': '','et': '','interation':   '','sst0': str(int(time.time() * 1000)),'page': str(self.page),'wxid': '','usip': ''},
                            method='get',
                            meta={'key':key,'maxNo':maxNo},
                            headers=self.headers,
                            callback=self.parse2)
            
    # 爬取每个文章的所需信息
    def parseArticleBody(self,response):
            item = WeixinSpiderItem()
            item['title'] = response.xpath("//div[@id='img-content']/h2[@class='rich_media_title']/text()").extract()[0].strip().replace('\r','').replace('\n','').replace('\t','')
            soup = BeautifulSoup(response.text, 'lxml')
            item['publishTime'] = soup.find('em',attrs={'class':'rich_media_meta rich_media_meta_text'}).get_text()
            item['article'] = soup.find('div', attrs={'class': 'rich_media_content '}).get_text()
            item['publicName'] = response.xpath("//a[@class='rich_media_meta rich_media_meta_link rich_media_meta_nickname']/text()").extract()[0]
            yield item


