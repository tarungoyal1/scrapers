# -*- coding: utf-8 -*-
import scrapy


class GetlisturlsSpider(scrapy.Spider):
    name = 'getlisturls'
    allowed_domains = ['www.goodreads.com']
    # start_urls = ['https://www.goodreads.com/list/tag/science-fiction']
    # start_urls = ['https://www.goodreads.com/list/tag/non-fiction']
    # start_urls = ['https://www.goodreads.com/list/tag/history']
    # start_urls = ['https://www.goodreads.com/list/tag/biography']
    # start_urls = ['https://www.goodreads.com/list/tag/contemporary']
    start_urls = ['https://www.goodreads.com/list/tag/sci-fi']

    # Bind this spider with it's own separate pipeline (ListUrlPipeline)
    custom_settings = {
        'ITEM_PIPELINES': {
            'goodreads_cralwer.pipelines.GetListUrlPipeLine': 400
        }
    }

    def parse(self, response):
        list_urls = response.xpath("//a[@class='listTitle']")
        for list_url in list_urls:
            yield {'list_url':response.urljoin(list_url.xpath(".//@href").get())}

        next_page = response.xpath("//a[@class='next_page']/@href").get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
