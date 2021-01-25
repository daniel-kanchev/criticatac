import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from criticatac.items import Article
from itemloaders.processors import TakeFirst


class CriticSpider(scrapy.Spider):
    name = 'critic'
    allowed_domains = ['criticatac.ro']
    start_urls = ['http://www.criticatac.ro/arhiva/']

    def parse(self, response):
        month_links = response.xpath("//a[@class='archive-month-title']/@href").getall()
        yield from response.follow_all(month_links, self.parse_month)

    def parse_month(self, response):
        article_links = response.xpath("//div[@class='entry-summary']/p/a/@href").getall()
        yield from response.follow_all(article_links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article(), response)
        item.default_output_processor = TakeFirst()

        title = response.xpath("//h1[@class='entry-title']/text()").get()
        author = response.xpath("//span[@class='author vcard']/a/text()").get()
        date = response.xpath("//span[@class='entry-date']/text()").get()
        date = format_date(date)
        content = response.xpath("(//div[@class='entry-content'])[1]//text()").getall()
        content = " ".join(content)

        item.add_value('title', title)
        item.add_value('author', author)
        item.add_value('date', date)
        item.add_value('content', content)
        item.add_value('link', response.url)

        return item.load_item()


def format_date(date):
    date_dict = {
        "ianuarie": "January",
        "februarie": "February",
        "martie": "March",
        "aprilie": "April",
        "mai": "May",
        "iunie": "June",
        "iulie": "July",
        "august": "August",
        "septembrie": "September",
        "octombrie": "October",
        "noiembrie": "November",
        "decembrie": "December",
    }

    date = date.split(" ")
    for key in date_dict.keys():
        if date[1] == key:
            date[1] = date_dict[key]
    date = " ".join(date)
    date_time_obj = datetime.strptime(date, '%d %B %Y')
    date = date_time_obj.strftime("%Y/%m/%d")
    return date
