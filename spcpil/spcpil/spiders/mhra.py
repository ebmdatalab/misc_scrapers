# -*- coding: utf-8 -*-
import re
import unicodedata

import scrapy
from spcpil.items import SpcpilItem

class MhraSpider(scrapy.Spider):
    name = 'mhra'
    allowed_domains = ['www.mhra.gov.uk']
    start_urls = ['http://www.mhra.gov.uk/spc-pil/']
    custom_settings = {
        'REDIRECT_ENABLED': False,
    }

    def parse(self, response):
        for second_level in response.xpath('//a[contains(@href, "secLevelIndexChar")]/@href'):
            url = response.urljoin(second_level.extract())
            yield scrapy.http.Request(
                url, callback=self.get_second_level)

    def get_second_level(self, response):
        for substance in response.xpath('//a[contains(@href, "subsName")]/@href'):
            url = response.urljoin(substance.extract())
            yield scrapy.http.Request(
                url, callback=self.get_substance_page)

    def get_substance_page(self, response):
        for product in response.xpath('//a[contains(@href, "prodName")]/@href'):
            url = response.urljoin(product.extract())
            yield scrapy.http.Request(
                url, callback=self.get_product_page)

    def get_product_page(self, response):
        # maybe just one spc and one pil for each page
        product_url = response.xpath('//a[contains(@href, "subsName")]/@href[1]').extract()[0]
        product = re.match(r".*subsName=(.*)&pageID=", product_url).groups()[0]
        seen_pil = seen_spc = False
        for leaflet in response.xpath('//ul[@class="searchResults"]//a[contains(@href, ".pdf")]'):
            href = leaflet.xpath('@href').extract_first()
            name = unicodedata.normalize("NFKD", leaflet.xpath('text()').extract_first()).strip()
            doc_type = 'spc' in name.lower() and 'SPC' or 'PIL'
            if doc_type == 'SPC':
                seen_spc = True
            if doc_type == 'PIL':
                seen_pil = True
            if seen_spc and seen_pil:
                return
            yield SpcpilItem(product=product, file_urls=[href], doc_type=doc_type, file_name=name)
