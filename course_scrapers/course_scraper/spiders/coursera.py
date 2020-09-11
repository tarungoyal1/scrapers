import scrapy
import json
from jsonpath_rw import jsonpath, parse


class CourseraSpider(scrapy.Spider):
    name = 'coursera'
    allowed_domains = ['www.coursera.org']

    # Bind this spider with it's own separate pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'course_scraper.pipelines.CourseraScraperPipeline': 400
        }
    }

    def start_requests(self):
        url = 'https://www.coursera.org/graphqlBatch?opname=catalogResultQuery'

        req_headers = {
            "content-type": "application/json",
            "x-csrf3-token": "1600603434.lk4901iV9X3SAv8R"
        }

        with open('requestdata.txt') as reader:
            additional_payload = reader.read()

        #computer-science
        #arts-and-humanities
        #data-science
        #personal-development
        #business
        #information-technology
        #life-sciences
        #math-and-logic
        #physical-science-and-engineering
        #social-sciences

        for i in range(0, 7):
            x = i*30
            payload = '[{{"operationName":"catalogResultQuery","variables":{{"skip":false,"limit":30,"facets":["skillNameMultiTag","jobTitleMultiTag","difficultyLevelTag","languages","productDurationEnum","entityTypeTag:Courses","partnerMultiTag","categoryMultiTag:{0}","subcategoryMultiTag","isPartOfCourseraPlus"],"sortField":"","start":"{1}"'
            payload = payload.format('language-learning',str(x))
            payload = payload+additional_payload
            yield scrapy.Request(url, method='POST', body=payload, headers=req_headers, dont_filter=True)

    def parse(self, response):
        
        category = "Language learning"

        data = json.loads(response.text)

        courseid_expr = parse('$..courses.elements[:].id')
        title_expr = parse('$..courses.elements[:].name')
        url_expr = parse('$..courses.elements[:].slug')
        partner_expr = parse('$..courses.elements[:].partners..name')
        skill_level_expr = parse("$..courses.elements[:].level")
        rating_expr = parse('$..courses.elements[:]..averageFiveStarRating')
        rating_count_expr = parse('$..courses.elements[:]..ratingCount')
        # role_expr = parse('$..roles.Values')
        duration_expr = parse('$..courses.elements[:]..avgLearningHoursAdjusted')
        thumbnail_expr = parse('$..courses.elements[:].photoUrl')

        course_id = [match.value for match in courseid_expr.find(data)]
        title = [match.value for match in title_expr.find(data)]
        url = [match.value for match in url_expr.find(data)]
        skill_level = [match.value for match in skill_level_expr.find(data)]
        partner = [match.value for match in partner_expr.find(data)]
        # date = [match.value for match in date_expr.find(data)]
        rating = [match.value for match in rating_expr.find(data)]
        rating_count = [match.value for match in rating_count_expr.find(data)]
        # role = [match.value for match in role_expr.find(data)]
        duration = [match.value for match in duration_expr.find(data)]
        thumbnail = [match.value for match in thumbnail_expr.find(data)]

        courses = {}

        course_list = []

        

        for i in range(len(course_id)):
            course = {}
            course['course_id'] = course_id[i]
            course['title'] = title[i]
            course['slug_url'] = url[i]

            try:
                course['skill_level'] = skill_level[i]
            except Exception as e:
                course['skill_level'] = ''

            try:
                course['partner'] = partner[i]
            except Exception as e:
                course['partner'] = ''

            try:
                course['rating'] = rating[i]
                course['rating_count'] = rating_count[i]
            except Exception as e:
                course['rating'] = 0
                course['rating_count'] = 0

            try:
                skill_exp_string = "$..courses.elements[{0}]..skillTags[:].skillName".format(i)
                skill_tags_expr = parse(skill_exp_string)
                course['skill_tags']  = [match.value for match in skill_tags_expr.find(data)]
            except Exception as e:
                course['skill_tags'] = []
            

            course['duration'] = duration[i]
            course['thumbnail'] = thumbnail[i]
            course['category'] = category

            course_list.append(course)

        courses['course_list'] = course_list
        # print(courses)

        yield courses
