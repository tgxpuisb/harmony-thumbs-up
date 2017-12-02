import scrapy
from app.items import ProjectItem


class ProjectSpider(scrapy.spiders.Spider):
    name = 'project'
    allowed_domains = ['github.com']
    start_urls = [
        'https://github.com/CoderSavior?tab=stars'
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="col-12 d-block width-full py-4 border-bottom"]'):
            project = ProjectItem()
            project['name'] = sel.xpath('div[1]/h3/a/@href').extract()[0].replace('/', '', 1)
            project['stars'] = sel.xpath('div[4]/a/text()').extract()[1].strip()
            project['forks'] = 0
            project['issues']= 0
            project['commits'] = 0
            project['create_time'] = 0
            yield project
        pass
