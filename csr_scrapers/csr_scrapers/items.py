# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CsrScrapersItem(scrapy.Item):
    study_id = scrapy.Field()
    clinical_study_id = scrapy.Field()
    clinicaltrials_id = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    sponsor = scrapy.Field()
    collaborators = scrapy.Field()
    phase = scrapy.Field()
    generic_name = scrapy.Field()
    trade_name = scrapy.Field()
    study_indication = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
# //table[@class="protocol_summary"]/tbody/tr[td[@class='rowlabel']]/td[contains(preceding-sibling::text(), 'C')]
