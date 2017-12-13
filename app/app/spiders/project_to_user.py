# 通过project来找寻点赞的人
# -*- coding: utf-8 -*-
import pymysql
from ..config import password, host, user, database
import scrapy
from app.items import UserItem
import time


class ProjectToUserSpider(scrapy.Spider):
    name = 'project_to_user'
    base_url = 'https://github.com/'
    allowed_domains = ['github.com']
    start_urls = []
    project_count = 0
    page_size = 1
    page = 1

    pid = 0

    def __init__(self):
        super()
        self.db = pymysql.connect(host, user, password, database)
        self.cursor = self.db.cursor()
        count_sql = 'SELECT id FROM project ORDER BY id DESC LIMIT 1'
        self.cursor.execute(count_sql)
        self.project_count = int(self.cursor.fetchone()[0])
        project = self.get_one_project()
        if project:
            self.pid = project[0]
            self.start_urls.append(self.base_url + project[1] + '/stargazers')

    def get_one_project(self):
        if self.project_count // self.page_size >= self.page:
            start_row = (self.page - 1) * self.page_size
            select_sql = "SELECT * FROM project LIMIT %s,%s" % (start_row, self.page_size)
            self.cursor.execute(select_sql)
            self.page += 1
            project = self.cursor.fetchone()
            return project
        else:
            return None

    def parse(self, response):

        for sel in response.xpath('//div[@id="repos"]/ol/li[@class="follow-list-item float-left border-bottom"]'):
            user_item = UserItem()
            user_item['name'] = sel.xpath('div[2]/h3/span/a/@href').extract_first().replace('/', '')
            info = sel.xpath('div[2]/p/text()').extract_first().strip()
            if info:
                info = info.replace('Joined on ', '')
                time_ary = time.strptime(info, "%b %d, %Y")
                user_item['create_time'] = int(time.mktime(time_ary))
            else:
                user_item['create_time'] = 0
            user_item['pid'] = self.pid
            yield user_item
        next_url_node = response.xpath('//div[@class="pagination"]/a[last()]')
        if next_url_node.xpath('text()').extract_first() == 'Next':
            next_url = next_url_node.xpath('@href').extract_first()
        else:
            next_url = None
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            project = self.get_one_project()
            print(project)
            if project:
                self.pid = project[0]
                yield scrapy.Request(url=self.base_url + project[1] + '/stargazers', callback=self.parse)

    def closed(self, reason):
        self.db.close()

# response.xpath('//div[@class="pagination"]/a/text()')

