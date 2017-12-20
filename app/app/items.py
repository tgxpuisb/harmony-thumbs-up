# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    name = scrapy.Field()
    stars = scrapy.Field()
    forks = scrapy.Field()
    commits = scrapy.Field()
    issues = scrapy.Field()
    create_time = scrapy.Field()
    pass


class UserItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    stars = scrapy.Field()
    follows = scrapy.Field()
    forks = scrapy.Field()
    following = scrapy.Field()
    create_time = scrapy.Field()
    # pid = scrapy.Field()
    repositories = scrapy.Field()
    pass



