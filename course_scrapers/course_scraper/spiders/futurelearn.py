import scrapy
import json
from jsonpath_rw import jsonpath, parse


class FuturelearnSpider(scrapy.Spider):
    name = 'futurelearn'
    allowed_domains = ['www.futurelearn.com']

    # Bind this spider with it's own separate pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'course_scraper.pipelines.FutureLearnScraperPipeline': 400
        }
    }
    

    def start_requests(self):
        # query = 'it-and-computer-science-courses'
        # query = 'business-and-management-courses'
        # query = 'creative-arts-and-media-courses'
        # query = 'healthcare-medicine-courses'
        # query = 'history-courses'
        # query = 'language-courses'
        # query = 'law-courses'
        # query = 'literature-courses'
        # query = 'nature-and-environment-courses'
        # query = 'psychology-and-mental-health-courses'
        # query = 'science-engineering-and-maths-courses'
        # query = 'study-skills-courses'
        query = 'teaching-courses'


        url = 'https://www.futurelearn.com/subjects/'+query+'?all_courses=1'

        req_headers = {
            'accept': 'application/json',
            'referer': 'https://www.futurelearn.com/subjects/'+query,
            'x-requested-with': 'XMLHttpRequest'
        }

        yield scrapy.Request(url, method='GET', headers=req_headers, dont_filter=True)


    def parse(self, response):
        # print(response.text)

        category = 'Teaching'
        tags = ["teaching", "parents", "development", "learning"]

        data = json.loads(response.text)

        courseid_expr = parse('$..cards..id')
        title_expr = parse('$..cards..title')
        url_expr = parse('$..cards..path')
        partner_expr = parse('$..cards[:].label')
        description_expr = parse("$..cards..introduction")
        rating_expr = parse('$..cards..averageReviewScore')
        rating_count_expr = parse('$..cards..totalReviews')
        duration_expr = parse('$..cards..numberOfWeeks')
        thumbnail_expr = parse('$..cards..imageUrl')

        course_id = [match.value for match in courseid_expr.find(data)]
        title = [match.value for match in title_expr.find(data)]
        url = [match.value for match in url_expr.find(data)]
        description = [match.value for match in description_expr.find(data)]
        partner = [match.value for match in partner_expr.find(data)]
        rating = [match.value for match in rating_expr.find(data)]
        rating_count = [match.value for match in rating_count_expr.find(data)]
        duration = [match.value for match in duration_expr.find(data)]
        thumbnail = [match.value for match in thumbnail_expr.find(data)]

        courses = {}

        course_list = []

        for i in range(len(course_id)):
            course = {}
            course['course_id'] = course_id[i]
            course['title'] = title[i]
            course['slug_url'] = url[i]
            course['description_expr'] = description[i]
            course['partner'] = partner[i]

            try:
                course['rating'] = rating[i]
                course['rating_count'] = rating_count[i]
            except Exception as e:
                course['rating'] = 0
                course['rating_count'] = 0

            course['duration'] = duration[i]
            course['thumbnail'] = thumbnail[i]
            course['category'] = category
            course['tags'] = tags

            course_list.append(course)

        courses['course_list'] = course_list
        # print(courses)

        yield courses
