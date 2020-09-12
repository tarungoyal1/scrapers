import scrapy
import json
from jsonpath_rw import jsonpath, parse


class HiristSpider(scrapy.Spider):
    name = 'hirist'
    allowed_domains = ['www.hirist.com']

    # Bind this spider with it's own separate pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'job_scrapers.pipelines.HiristPipeline': 400
        }
    }


    def start_requests(self):

        sector = "IT"
        profile = 'Backend Developer'
        portal_technology = 'Spring'
        skill_tags = ['spring','java','backend', 'developer']
        portal = 'Hirist'

        metadata = {
            "sector":sector,
            "profile": profile,
            "portal_tech":portal_technology,
            "skill_tags":skill_tags,
            "portal":portal
        }

        limit = 9
        query_id = 47

        for i in range(limit):
            url = 'https://jobseeker-api.hirist.com/jobfeed/-1/jobs?pageNo='+str(i)+'&sort=date&query='+str(query_id)
            yield scrapy.Request(url, method='GET', meta=metadata, dont_filter=True)



    def parse(self, response):
        # print(response.text)

        data = json.loads(response.text)

        jobid_expr = parse('$.jobs[:].id')
        jobtitle_expr = parse('$.jobs..title')
        location_expr = parse('$.jobs..location')
        companyData_expr = parse('$.jobs..companyData')
        minExperience_expr = parse('$.jobs..min')
        maxExperience_expr = parse('$.jobs..max')
        timeCreated_expr = parse('$.jobs..createdTime')
        applyURL_expr = parse('$.jobs..applyUrl')

        job_id = [match.value for match in jobid_expr.find(data)]
        title = [match.value for match in jobtitle_expr.find(data)]
        location = [match.value for match in location_expr.find(data)]
        companyData = [match.value for match in companyData_expr.find(data)]
        minExp = [match.value for match in minExperience_expr.find(data)]
        maxExp = [match.value for match in maxExperience_expr.find(data)]
        timeCreated = [match.value for match in timeCreated_expr.find(data)]
        applyURL = [match.value for match in applyURL_expr.find(data)]

        jobs = {}

        jobs_list = []

        for i in range(len(job_id)):

            job = {}

            job['job_id'] = job_id[i]
            job['title'] = title[i]
            job['location'] = location[i]
            job['companyData'] = companyData[i]
            job['minExp'] = minExp[i]
            job['maxExp'] = maxExp[i]
            job['timeCreated'] = timeCreated[i]
            job['applyURL'] = applyURL[i]

            job['sector'] = response.meta['sector']
            job['profile'] = response.meta['profile']
            job['skill_tags'] = response.meta['skill_tags']
            job['portal'] = response.meta['portal']

            jobs_list.append(job)

        jobs['job_list'] = jobs_list

        yield jobs

