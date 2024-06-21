# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DomRfItem(scrapy.Item):
    title = scrapy.Field()
    address = scrapy.Field()
    id_ad = scrapy.Field()
    commissioning = scrapy.Field()
    developer = scrapy.Field()
    group_companies = scrapy.Field()
    date_publication_project = scrapy.Field()
    key_issuance = scrapy.Field()
    average_price_per1m = scrapy.Field()
    sale_apartments = scrapy.Field()
    real_estate_class = scrapy.Field()
    number_apartments = scrapy.Field()
