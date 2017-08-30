# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ScrapycrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item



from pymongo import MongoClient

class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['corpfinder']
        self.collection = self.db['corpInfo']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.collection
        checkData = {'target_corp':item['target_corp'], 'url':item['url']}
        if collection.find(checkData):
            collection.delete_many(checkData)

        collection.insert_one(dict(item))

        return item