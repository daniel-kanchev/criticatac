import scrapy


class CriticSpider(scrapy.Spider):
    name = 'critic'
    allowed_domains = ['criticatac.ro']
    start_urls = ['http://criticatac.ro/']

    def parse(self, response):
        pass
