import scrapy
import json
from jsonpath_rw import jsonpath, parse


class PluralsightSpider(scrapy.Spider):
    name = 'pluralsight'
    allowed_domains = ['www.pluralsight.com']

    # Bind this spider with it's own separate pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'course_scraper.pipelines.PluralsightScraperPipeline': 400
        }
    }


    def start_requests(self):
    	url = 'https://api-us1.cludo.com/api/v3/10000847/10001374/search'
    	
    	req_headers = {
    		"authorization": "SiteKey MTAwMDA4NDc6MTAwMDEzNzQ6U2VhcmNoS2V5",
    		"Content-Type": "application/json; charset=UTF-8"
    	}

    	query = "Maya"
    	pagination = 9

    	for i in range(pagination):

    		payload = '''
    			{{"ResponseType":"json","query":"{0}","facets":{{"categories":["course"]}},"enableFacetFiltering":"true","operator":"and","page":{1},"perPage":100}}
    		'''

    		payload = payload.format(query,i)


    		yield scrapy.Request(url, method='POST', body=payload, headers=req_headers, dont_filter=True)
 

    def parse(self, response):

    	subcategory = "Maya"

    	category = ["Manufacturing", "Design"]


    	data = json.loads(response.text)

    	title_expr = parse('$..Title.Value')
    	url_expr = parse('$..Url.Value')
    	skill_level_expr = parse("$..['Skill Levels'].Value")
    	author_expr = parse('$..authors.Value')
    	date_expr = parse('$..cludo-date.Value')
    	rating_expr = parse('$..rating.Value')
    	rating_count_expr = parse('$..rating-count.Value')
    	role_expr = parse('$..roles.Values')
    	duration_expr = parse('$..duration.Value')
    	thumbnail_expr = parse('$..thumbnail.Value')
    	

    	title = [match.value for match in title_expr.find(data)]
    	url = [match.value for match in url_expr.find(data)]
    	skill_level = [match.value for match in skill_level_expr.find(data)]
    	author = [match.value for match in author_expr.find(data)]
    	date = [match.value for match in date_expr.find(data)]
    	rating = [match.value for match in rating_expr.find(data)]
    	rating_count = [match.value for match in rating_count_expr.find(data)]
    	role = [match.value for match in role_expr.find(data)]
    	duration = [match.value for match in duration_expr.find(data)]
    	thumbnail = [match.value for match in thumbnail_expr.find(data)]

    	courses = {}

    	course_list = []


    	for i in range(len(title)):
    		course = {}
    		course['title'] = title[i]
    		course['url'] = url[i]
    		course['skill_level'] = skill_level[i]
    		course['author'] = author[i]
    		course['date'] = date[i]
    		try:
    			course['rating'] = rating[i]
    			course['rating_count'] = rating_count[i]
    			course['role'] = role[i]
    		except Exception as e:
    			course['rating'] = 0
    			course['rating_count'] = 0
    			course['role'] = ''
    		course['duration'] = duration[i]
    		course['thumbnail'] = thumbnail[i]
    		course['category'] = category
    		course['subcategory'] = subcategory

    		course_list.append(course)


    	courses['course_list'] = course_list
    	
    	yield courses
