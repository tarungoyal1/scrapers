# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


class HiristPipeline:
    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['india_jobs']
        self.col_hirirst_jobs = self.db['hirist_jobs']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        # print(item)
        if item:
            if self.col_hirirst_jobs.insert_many(item['job_list']):
                return "{} jobs have been added.".format(len(item['job_list']))
