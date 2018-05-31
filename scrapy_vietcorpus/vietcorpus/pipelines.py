# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
logger = logging.getLogger(__name__)

from redis import Redis


r = Redis()
redis_queue = "viet_search_results"

class WriteToRedis(object):
    def process_item(self, item, spider):
        r.rpush(redis_queue, item)
        logger.info(f"Writing result to redis: {dict(item)}")
        return item
