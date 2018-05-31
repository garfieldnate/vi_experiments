# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SearchResultItem(Item):
    # query string
    query = Field()
    # rank on (first) page
    rank = Field()
    # search result URL
    result_url = Field()

    # housekeeping
    search_url = Field()
    date = Field()
