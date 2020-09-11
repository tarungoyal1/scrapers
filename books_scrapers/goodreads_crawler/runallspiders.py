from scrapy.crawler import CrawlerProcess
from goodreads_cralwer.spiders.singlelistscrape import SinglelistcrawlSpider
from goodreads_cralwer.spiders.get_book_details import GetBookDetailsSpider

process = CrawlerProcess()
process.crawl(SinglelistcrawlSpider)
# process.crawl(GetBookDetailsSpider)
process.start()