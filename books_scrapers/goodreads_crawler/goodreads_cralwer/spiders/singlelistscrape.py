# -*- coding: utf-8 -*-
import scrapy
from .geturls import get_listurl, updateListStatus
import logging


class SinglelistcrawlSpider(scrapy.Spider):
    name = 'singlelistcrawl'
    allowed_domains = ['www.goodreads.com']

    # Bind this spider with it's own separate pipeline (BookUrlPipeline)
    custom_settings = {
        'ITEM_PIPELINES': {
            'goodreads_cralwer.pipelines.BookUrlPipeline': 400
        }
    }


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler, *args, **kwargs)
        crawler.signals.connect(spider.idle_consume, scrapy.signals.spider_idle)
        return spider

    def __init__(self, crawler):
        self.crawler = crawler

    def start_requests(self):
        urls_batch = get_listurl()
        urls = next(urls_batch)
        for i in range(1):
            yield scrapy.Request(urls.pop(0))

    def idle_consume(self):
        """
        Everytime spider is about to close check our urls
        buffer if we have something left to crawl
        """
        reqs = self.start_requests()
        if not reqs:
            return
        logging.info('Consuming batch')
        for req in reqs:
            # print(req)
            self.crawler.engine.schedule(req, self)
        raise scrapy.exceptions.DontCloseSpider


    def parse(self, response):
        # book_url = {
        #     'url': '',
        #     'status': 'pending'
        # }

        scraped_book_urls = {'scraped_urls':[]}

        for url in response.xpath("//table[contains(@class, 'tableList')]//tr"):
            scraped_book_urls['scraped_urls'].append(response.urljoin(url.xpath(".//a[@class='bookTitle']/@href").get()))
            # book_url['url'] = response.urljoin(url.xpath(".//a[@class='bookTitle']/@href").get())
        yield scraped_book_urls

        next_page = response.xpath("//div[@class='pagination']//a[@class='next_page']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            # means reached the last page in pagination
            last_url = response.request.url.partition('?')[0]
            if updateListStatus(last_url):
                print("List fully scraped and status changed to 'done', list_url = {}".format(last_url))



