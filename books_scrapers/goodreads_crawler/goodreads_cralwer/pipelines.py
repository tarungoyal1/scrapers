# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

#This pipeline is bound with spider = GetBookDetailsSpider in get_book_details.py
class GoodreadsCralwerPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books']
        self.col_bookinfo = self.db['book_info']
        self.col_allbookurls = self.db['book_urls']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print('GoodreadsCralwerPipeline')
        if not self.col_bookinfo.find_one({'book_url': item['book_url']}):
            if self.col_bookinfo.insert_one(item):
                if self.col_allbookurls.update_one({'url': item['book_url']}, {'$set': {'status': 'done'}},upsert=False).modified_count == 1:
                    # print('New book inserted and status updated, url  = {}'.format(item['book_url']))
                    return True
        elif self.col_allbookurls.update_one({'url': item['book_url']}, {'$set': {'status': 'done'}},upsert=False).modified_count == 1:
            # print('Book already scraped having url = {}'.format(item['book_url']))
            return True
        return False



#This pipeline is bound with spider = GrlistcrawlSpider in grlistcrawl.py
class BookUrlPipeline:
    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books']
        self.col_bookurls = self.db['book_urls'] # Old collection having book urls of non-fiction

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        #Returned 'item' is a dictionary containing a list of scraped urls on a single page of list inside key=  'scraped_urls'

        # print(item['scraped_urls'])

        #Effecient code with aggregation pipeline and use setDifference to get only non-existing book urls to be inserted

        pipeline = [
            { "$group": { "_id": 'null', 'values': { "$push": "$url" } } },
            { "$project":
                  { 'non_existing':
                        { "$setDifference": [item['scraped_urls'], "$values"]}
                  }
            }
        ]

        non_exitng_urls = list(self.col_bookurls.aggregate(pipeline))[0]['non_existing']
        count = len(non_exitng_urls)
        # print(non_exitng_urls)

        #Now you can bulk insert with just one query
        if count>0:
            if self.col_bookurls.insert_many([{'url': url, 'status':'pending'} for url in non_exitng_urls]):
                print('Inserted {} new book urls'.format(count))
                return True
        return False

        #Achievement: Now, for every page of list there would only execute exactly 2 queries
        # One for setDifference and other for bulk insert



        #Ineffecient code because it checks for every url in a loop
        # if not self.col_bookurls.find_one({'url': item['url']}):
        #     if  self.col_bookurls.update_one(item,{'$set':item},upsert=True):
        #         print('New book url inserted, url ={}'.format(item['url']))
        #         return True
        # else:
        #     return False
        # return False

#This pipeline is bound with spider = GetlisturlsSpider in getlisturls.py
class GetListUrlPipeLine:
    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books']
        self.col_listurls = self.db['list_urls']


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not self.col_listurls.find_one({'list_url': item['list_url']}):
            if  self.col_listurls.update_one(item,{'$set':item},upsert=True):
                print('New list url inserted, url ={}'.format(item['list_url']))
                return True
        else:
            return False
        return False
