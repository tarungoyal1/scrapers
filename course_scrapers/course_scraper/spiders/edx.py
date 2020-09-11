import scrapy
import json
import time
from jsonpath_rw import jsonpath, parse


class EdxSpider(scrapy.Spider):
    name = 'edx'
    allowed_domains = ['www.edx.org']


    # Bind this spider with it's own separate pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'course_scraper.pipelines.EDXScraperPipeline': 400
        }
    }


    def start_requests(self):
        url = 'https://igsyv1z1xi-3.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.0.3)%3B%20Browser%20(lite)%3B%20react%20(16.13.1)%3B%20react-instantsearch%20(6.3.0)%3B%20JS%20Helper%20(3.1.1)&x-algolia-api-key=448c9e20c867b4a3f602687b5ec33890&x-algolia-application-id=IGSYV1Z1XI'

        req_headers = {
            "content-type": "application/x-www-form-urlencoded"
        }

        with open('edx_request_data1.txt') as reader:
            first_payload = reader.read()

        with open('edx_request_data2.txt') as reader:
            additional_payload = reader.read()

        for i in range(6, 43):
            page = i
            payload = first_payload + '&page=' + str(page)
            payload = payload + additional_payload
            yield scrapy.Request(url, method='POST', body=payload, headers=req_headers, meta={"page": page}, dont_filter=True)
            time.sleep(5)

    def parse(self, response):
        # print(response.text)

        data = json.loads(response.text)


        # page_num = response.meta['page']
        page_num = 1

        courseid_expr = parse('$..results[{0}]..uuid'.format(page_num))
        title_expr = parse('$..results[{0}]..title.value'.format(page_num))
        url_expr = parse('$..results[{0}]..marketing_url'.format(page_num))
        owner_expr = parse('$..results[{0}]..owners[0].name'.format(page_num))
        subject_expr = parse('$..results[{0}]..subject'.format(page_num))
        level_expr = parse('$..results[{0}]..level'.format(page_num))
        description_expr = parse('$..results[{0}]..primary_description.value'.format(page_num))
        enroll_count_expr = parse('$..results[{0}]..recent_enrollment_count'.format(page_num))
        thumbnail_expr = parse('$..results[{0}]..card_image_url'.format(page_num))

        course_id = [match.value for match in courseid_expr.find(data)]
        title = [match.value for match in title_expr.find(data)]
        urls = [match.value for match in url_expr.find(data)]
        owner = [match.value for match in owner_expr.find(data)]
        subject = [match.value for match in subject_expr.find(data)]
        skill_level = [match.value for match in level_expr.find(data)]
        description = [match.value for match in description_expr.find(data)]
        enrollment = [match.value for match in enroll_count_expr.find(data)]
        thumbnail = [match.value for match in thumbnail_expr.find(data)]

     
        courses = {}

        course_list = []

        category = "Computer Science"

        for i in range(len(course_id)):
            course = {}
            course['course_id'] = course_id[i]
            course['title'] = title[i]
            course['slug_url'] = urls[i]

            try:
                course['skill_level'] = skill_level[i][0]
            except Exception as e:
                course['skill_level'] = ''

            try:
                course['owner'] = owner[i]
            except Exception as e:
                course['owner'] = ''


            try:
                course['skill_tags']  = subject[i]
            except Exception as e:
                course['skill_tags'] = []
            

            course['enroll_count'] = enrollment[i]
            course['description'] = description[i]
            course['thumbnail'] = thumbnail[i]
            course['category'] = category

            course_list.append(course)

        courses['course_list'] = course_list
        # print(courses)

        yield courses
