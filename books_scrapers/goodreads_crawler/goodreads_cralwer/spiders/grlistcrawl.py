# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup, NavigableString
import re

#This spider crawls the links of books but don't visit them
#It's purpose is to jusr obtain book link(s) and save them in book_urls collections

class GrlistcrawlSpider(CrawlSpider):
    name = 'grlistcrawl'

    #Bind this spider with it's own separate pipeline (BookUrlPipeline)
    custom_settings = {
        'ITEM_PIPELINES': {
            'goodreads_cralwer.pipelines.BookUrlPipeline': 400
        }
    }

    allowed_domains = ['www.goodreads.com']
    start_urls = ['https://www.goodreads.com/list/tag/romance']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='listTitle']"), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='next_page']")),
    )

    def parse_item(self, response):
        book_url = {
            'url': '',
            'status':'pending'
        }

        for url in response.xpath("//table[contains(@class, 'tableList')]//tr"):
            book_url['url'] = response.urljoin(url.xpath(".//a[@class='bookTitle']/@href").get())
            yield book_url
