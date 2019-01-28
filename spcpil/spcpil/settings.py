# -*- coding: utf-8 -*-

# Scrapy settings for spcpil project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spcpil'

SPIDER_MODULES = ['spcpil.spiders']
NEWSPIDER_MODULE = 'spcpil.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'ebmdatalab.net scraper'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 5
EXTENSIONS = {
    'scrapy.extensions.closespider.CloseSpider': None,
}
ITEM_PIPELINES = {
    'scrapy.pipelines.files.FilesPipeline': 1,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 2}
FILES_STORE = 'gs://ebmdatalab/spcpil/'
GCS_PROJECT_ID = 'ebmdatalab'
CLOSESPIDER_ITEMCOUNT = 10
FEED_EXPORTERS = {
    'sqlite': 'spcpil.exporters.SqliteItemExporter'
}
