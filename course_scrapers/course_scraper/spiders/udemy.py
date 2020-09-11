import scrapy
import json
from jsonpath_rw import jsonpath, parse




class UdemySpider(scrapy.Spider):
    name = 'udemy'
    allowed_domains = ['www.udemy.com']
    # start_urls = ['https://www.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&category_id=288&source_page=category_page&locale=en_US&currency=inr&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat']

    
    # Bind this spider with it's own separate pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'course_scraper.pipelines.UdemySraperPipeline': 400
        }
    }

    def start_requests(self):
    	url = 'https://www.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&category_id=300&source_page=category_page&locale=en_US&navigation_locale=en_US&sos=pc&fl=cat&page='
    	for i in range(1, 626):
        	yield scrapy.Request(url+str(i), dont_filter=True)


    def parse(self, response):
    	#course_urls = response.xpath("//div[contains(@class, 'course-list--container')]//div[contains(@class, 'course-card--container')]")
    	
    	#print(response.text)

    	data = json.loads(response.text)

    	id_expr = parse('$..items[:].id')
    	url_expr = parse('$..items[:].url')
    	title_expr = parse('$..items[:].title')
    	headline_expr = parse('$..items[:].headline')
    	num_subscribers_expr = parse('$..items[:].num_subscribers')
    	avg_rating_expr = parse('$..items[:].avg_rating')
    	review_count_expr = parse('$..items[:].num_reviews')
    	published_time_expr = parse('$..items[:].published_time')
    	objectives_summary_expr = parse('$..items[:].objectives_summary')
    	content_info_expr = parse('$..items[:].content_info')
    	level_expr = parse('$..items[:].instructional_level')
    	img_url_expr = parse('$..items[:].image_750x422')


    	ids = [match.value for match in id_expr.find(data)]
    	urls = [match.value for match in url_expr.find(data)]
    	title = [match.value for match in title_expr.find(data)]
    	headline = [match.value for match in headline_expr.find(data)]
    	num_subscribers = [match.value for match in num_subscribers_expr.find(data)]
    	review_count = [match.value for match in review_count_expr.find(data)]
    	published_time = [match.value for match in published_time_expr.find(data)]
    	objectives_summary = [match.value for match in objectives_summary_expr.find(data)]
    	content_info = [match.value for match in content_info_expr.find(data)]
    	instructional_level = [match.value for match in level_expr.find(data)]
    	img_url = [match.value for match in img_url_expr.find(data)]


    	courses = {}

    	course_list = []

    	for i in range(len(ids)):
    		course = {}
    		course['course_id'] = ids[i]
    		course['url'] = 'https://udemy.com'+urls[i]
    		course['title'] = title[i]
    		course['headline'] = headline[i]
    		course['num_subscribers'] = num_subscribers[i]
    		course['review_count'] = review_count[i]
    		course['published_time'] = published_time[i]
    		course['objectives_summary'] = objectives_summary[i]
    		course['content_info'] = content_info[i]
    		course['inst_level'] = instructional_level[i]
    		course['img_url'] = img_url[i]
    		course['category'] = 'teaching & academics'

    		course_list.append(course)


    	courses['course_list'] = course_list
    	#return list to pipeline for bulk insert

    	yield courses