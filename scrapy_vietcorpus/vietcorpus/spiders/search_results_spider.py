# -*- coding: utf-8 -*-
import datetime
from os import path
from urllib.parse import urlencode, urlparse, parse_qs

import scrapy
import redis

from vietcorpus.items import SearchResultItem

redis = redis.Redis()
dir_path = path.dirname(path.realpath(__file__))
duckduckgo_url = "https://duckduckgo.com/html/?"

class SearchResultsSpider(scrapy.Spider):
    name = 'duckduckgo_seeds'
    allowed_domains = ['duckduckgo']
    query_file = path.realpath(f"{dir_path}/../../../web_corpus/wiki_keywords/queries_30000.txt")
    with open(query_file) as f:
        queries = f.read().splitlines()
    start_urls = [duckduckgo_url + urlencode({'q': q,
        'kp': -2, # no safe search
        'kd': -2 # don't use redirect URLs
    }) for q in queries]
    print(f"Created URLs from {query_file}; example formatted URL: {start_urls[0]}")

    def parse(self, response):
        for rank, result_selector in enumerate(response.css("#links .result__a").xpath('@href')):
            item = SearchResultItem()
            item['query'] = parse_qs(urlparse(response.url).query)['q'][0]
            item['rank'] = rank
            item['result_url'] = result_selector.extract()

            item['date'] = datetime.datetime.now()
            item['search_url'] = response.url

            yield item



