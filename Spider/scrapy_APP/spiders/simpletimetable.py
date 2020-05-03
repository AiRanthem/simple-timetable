from scrapy_APP.scrapy_redis.spiders import RedisSpider
from scrapy_APP.utils.SeleniumUtils import SsfwExtractor
from scrapy_APP.items import TableItem

import scrapy

from scrapy_APP.config import USERNAME, PASSWORD
import pickle
import os


class SimpleTimetableSpider(RedisSpider):
    name = 'simple_timetable'
    redis_key = 'simple:start_urls'
    allowed_domains = ['xmu.edu.cn', 'baidu.com']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = SsfwExtractor()

    def parse(self, response):
        table = self.extractor.testFor()

        item = TableItem()
        item['tableList'] = table
        yield item






