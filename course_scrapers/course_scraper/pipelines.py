# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from pymongo import MongoClient


class UdemySraperPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['courses']
        self.col_udemy_courses = self.db['udemy_courses']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #item -> courses list with each course as dict


        # return item

        # print(item)
        if item:
            if self.col_udemy_courses.insert_many(item['course_list']):
                return "{} courses have been added.".format(len(item['course_list']))


class PluralsightScraperPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['courses']
        self.col_pluralsight_courses = self.db['pluralsight_courses']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #item -> courses list with each course as dict


        if item:
            if self.col_pluralsight_courses.insert_many(item['course_list']):
                return "{} courses have been added.".format(len(item['course_list']))

class CourseraScraperPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['courses']
        self.col_coursera_courses = self.db['coursera_courses']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #item -> courses list with each course as dict


        if item:
            if self.col_coursera_courses.insert_many(item['course_list']):
                return "{} courses have been added.".format(len(item['course_list']))

class EDXScraperPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['courses']
        self.col_edx_courses = self.db['edx_courses']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #item -> courses list with each course as dict


        if item:
            if self.col_edx_courses.insert_many(item['course_list']):
                return "{} courses have been added.".format(len(item['course_list']))

class FutureLearnScraperPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['courses']
        self.col_futurelearn_courses = self.db['fl_courses']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #item -> courses list with each course as dict


        if item:
            if self.col_futurelearn_courses.insert_many(item['course_list']):
                return "{} courses have been added.".format(len(item['course_list']))




