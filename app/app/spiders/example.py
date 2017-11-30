# -*- coding: utf-8 -*-
import scrapy
from app.items import AppItem

class ExampleSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/CoderSavior']

    def parse(self, response):
        # print(response.body)
        for sel in response.xpath('//a[@title=\'Stars\']'):
            print(1)
            print(sel.xpath('@href').extract())
        pass