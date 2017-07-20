"""
Pull all available practice email addresses
"""

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest
import scrapy
from csr_scrapers.items import CsrScrapersItem
import logging
import json


class NovoNordiskSpider(Spider):
    name = "novonordisk"
    start_urls = ["http://www.novonordisk-trials.com/SearchService/TrialSearch.ashx?Command=Search&IsCSRAvailable=true"]

    def parse(self, response):
         jsonresponse = json.loads(response.body_as_unicode())
         for j in jsonresponse:
             item = CsrScrapersItem()
             item['study_id'] = j['TrialId']
             item['phase'] = j['Phase']
             item['created_at'] = j['StartDate']
             item['updated_at'] = j['UpdatedDate']
             item['title'] = j['Title']
             item['generic_name'] = j['TreatmentSummary']
             details_link = "http://www.novonordisk-trials.com/SearchService/TrialSearch.ashx?Command=GetTrialDetail&TrialId=%s&Index=0&Tab=result" % item['study_id']
             request = scrapy.Request(details_link, callback=self.parse_url_from_details)
             request.meta['item'] = item
             yield request

    def parse_url_from_details(self, response):
        item = response.meta['item']
        jsonresponse = json.loads(response.body_as_unicode())
        link1 = response.urljoin(jsonresponse['TrialResult']['SummaryOfTrialResults'][1]['Location'])
        link2 = response.urljoin(jsonresponse['TrialResult']['SummaryOfTrialResults'][0]['Location'])
        item['file_urls'] = [link1, link2]
        return item
