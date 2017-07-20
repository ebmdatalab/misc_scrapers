"""
Pull all available practice email addresses
"""

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest
import scrapy
from csr_scrapers.items import CsrScrapersItem
import logging


class GSKSpider(Spider):
    name = "gsk"
    start_urls = ["http://www.gsk-clinicalstudyregister.com/search/"]

    def parse(self, response):
        return FormRequest.from_response(
            response,
            formnumber=2,
            formdata={'document_type': '28'},
            callback=self.parse_reports_follow_next_page)

    def parse_reports_follow_next_page(self, response):
        for study_url in response.xpath(
                '//*[@id="fullWidthContent"]/div[2]/div/table/tbody/tr//td[1]/a/@href'):
            url = response.urljoin(study_url.extract())
            yield scrapy.http.Request(url, self.grab_pdf)

        next_page = response.xpath('//*[@id="pagination"]/li[@class="activepage"]/following-sibling::li[1]/a/@href')
        if next_page:
            logging.info( "Next page...")
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_reports_follow_next_page)

    def grab_pdf(self, response):
        md_headings = {
            'study_id' : 'Study ID',
            'clinical_study_id': 'Clinical Study ID',
            'title': 'Study Title',
            'sponsor': 'Sponsor',
            'collaborators': 'Collaborators',
            'phase': 'Phase',
            'generic_name': 'Generic Name',
            'trade_name': 'Trade Name',
            'study_indication': 'Study Indication'
        }
        md = {}
        md_xpath = "//table[@class='protocol_summary']//tr[td[@class='rowlabel']]/td[contains(preceding-sibling::td//text(), '%s')]//text()"
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        for k, v in md_headings.items():
            hit = response.xpath(md_xpath % v).extract()
            if hit:
                md[k] = hit[0].strip()
        md['created_at'] = response.xpath("//div[@id='csr']//td[@class='WhiteRowColumn1'][2]//text()")[0].extract()
        md['updated_at'] = response.xpath("//div[@id='csr']//td[@class='WhiteRowColumn1'][3]//text()")[0].extract()
        md['file_urls'] = [response.urljoin(response.xpath('//*[@id="csr"]/table//tr/td[1]/ul/li/a/@href')[0].extract())]
        yield CsrScrapersItem(**md)
