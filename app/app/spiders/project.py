import scrapy
from app.items import ProjectItem


class ProjectSpider(scrapy.Spider):
    name = 'project'
    base_url = 'https://github.com'
    allowed_domains = ['github.com']
    start_urls = [
        'https://github.com/CoderSavior?tab=stars'
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="col-12 d-block width-full py-4 border-bottom"]'):
            stars = sel.xpath('div[4]/a/text()').extract()[1].strip()
            if 10 < int(stars) < 1000:
                # 如果项目的stars数量在10到1000之间则要记录
                project = ProjectItem()
                project['name'] = sel.xpath('div[1]/h3/a/@href').extract()[0].replace('/', '', 1)
                project['stars'] = sel.xpath('div[4]/a/text()').extract()[1].strip()
                project['forks'] = 0
                project['issues'] = 0
                project['commits'] = 0
                project['create_time'] = 0
                yield project

        next_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
        print(next_url)
        if next_url:
            yield scrapy.Request(url=self.base_url + next_url, callback=self.parse)
