"""
Pull all available practice email addresses
"""

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest
import scrapy
from csr_scrapers.items import CsrScrapersItem
import logging


class BayerSpider(Spider):
    name = "bayer"
    start_urls = ["http://pharma.bayer.com/en/innovation-partnering/clinical-trials/trial-finder/?page=1&num=10&num=1000&search=&product=&overall_status=&country=&phase=&condition=&results=1&trials=0&btnSubmit=submit&show=1"]

    def parse(self, response):
        return self.parse_reports_follow_next_page(response)

    def parse_reports_follow_next_page(self, response):
        for study_url in response.xpath(
                '//table[@class="trialFinder"]//tr/td[1]/a/@href'):
            url = response.urljoin(study_url.extract())
            yield scrapy.http.Request(url, self.grab_pdf)

        next_page = response.xpath("//div[contains(@class, 'pagination')]//a[img[contains(@src, 'but_suche_vor')]]/@href")
        if next_page:
            logging.info( "Next page...")
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_reports_follow_next_page)

    def grab_pdf(self, response):
        md_headings = {
            'study_id' : 'Trial ID',
            'title': 'Official Title',
            'sponsor': 'Sponsor',
            'generic_name': 'Product',
            'study_indication': 'Indication/Disease',
        }
        md = {}
        md_xpath = "//table[@class='text']//tr[td[@class='texttuerkisfett']]/td[contains(preceding-sibling::td//text(), '%s')]//text()"
        for k, v in md_headings.items():
            hit = response.xpath(md_xpath % v).extract()
            if hit:
                md[k] = hit[0].strip()
        md['file_urls'] = response.xpath("//table[@class='text']//tr[td[@class='texttuerkisfett']]/td[contains(preceding-sibling::td//text(), '%s')]//a/@href" % "Results Synopsis").extract()

        yield CsrScrapersItem(**md)
