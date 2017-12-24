# 用户详细信息
import scrapy
from ..config import password, host, user as user_account, database
from app.items import UserItem
import pymysql


class UserDetail(scrapy.Spider):

    name = 'user_detail'
    base_url = 'https://github.com/'
    allowed_domains = ['github.com']
    start_urls = []
    user_count = 0
    page_size = 1
    page = 937
    handle_httpstatus_list = [404, 500, 503]

    uid = 0

    def __init__(self):
        super()
        self.db = pymysql.connect(host, user_account, password, database)
        self.cursor = self.db.cursor()
        count_sql = 'SELECT id FROM `user` ORDER BY id DESC LIMIT 1'
        self.cursor.execute(count_sql)
        self.user_count = int(self.cursor.fetchone()[0])

        user = self.get_one_user()
        if user:
            self.uid = user[0]
            self.start_urls.append(self.base_url + user[1])

    def get_one_user(self):
        if self.user_count // self.page_size >= self.page:
            start_row = (self.page - 1) * self.page_size
            select_sql = "SELECT * FROM `user` LIMIT %s,%s" % (start_row, self.page_size)
            self.cursor.execute(select_sql)
            self.page += 1
            print('page:')
            print(self.page)
            user = self.cursor.fetchone()
            return user
        else:
            return None

    def parse(self, response):

        def k2num(num):
            if num.endswith('k'):
                return str(float(num.replace('k', '')) * 1000)
            else:
                return num

        if response.status in self.handle_httpstatus_list:
            print('404')
        else:
            user_item = UserItem()
            user_item['id'] = self.uid
            count_nodes = response.xpath('//span[@class="Counter"]/text()')
            if count_nodes and len(count_nodes) == 4:
                user_item['repositories'] = k2num(count_nodes[0].extract().strip())
                user_item['stars'] = k2num(count_nodes[1].extract().strip())
                user_item['follows'] = k2num(count_nodes[2].extract().strip())
                user_item['following'] = k2num(count_nodes[3].extract().strip())
            yield user_item

        user = self.get_one_user()
        if user:
            self.uid = user[0]
            next_url = self.base_url + user[1]
            yield scrapy.Request(url=next_url, callback=self.parse)

    def closed(self):
        self.db.close()

    pass

# response.xpath('//span[@class="Counter"]/text()')[1].extract().strip()