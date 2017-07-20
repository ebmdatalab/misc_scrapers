"""Thing
"""
import scrapy

from nhschoices.items import PracticeItem


class PracticesSpider(scrapy.Spider):
    """A spider to scrape practices from NHS Choices
    """
    name = "practices"
    allowed_domains = ["www.nhs.uk"]
    custom_settings = {
        'REDIRECT_ENABLED': False,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.01,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 20,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 20,
        'AUTOTHROTTLE_DEBUG': True
    }

    def start_requests(self):
        for page_id in range(0, 111000):
            url = ("http://www.nhs.uk/Services/GP/MapsAndDirections/"
                   "DefaultView.aspx?id=%s" % page_id)
            yield scrapy.http.Request(
                url, callback=self.get_profile)

    def get_profile(self, response):
        """Get profile from each page
        """
        # <meta name="DCSext.PIMS_orgkey" content="Jessop Medical Practice_C81005"></meta>

        meta = response.xpath('//meta[@name="DCSext.PIMS_orgkey"]/@content')[0].extract()
        official_name, code = meta.split("_")
        datum = {
            'name': official_name,
            'code': code
        }
        self.logger.warning("%s, %s" % (official_name, code))
        try:
            contacts = response.xpath(
                '//*[@id="ctl00_ctl00_ctl00_PlaceHolderMain_contentColumn1"]'
                '/div[1]/div/div/div[1]')[0]
        except IndexError:
            hidden = not not response.xpath(
                "//*[@id='aliasbox']/h1[text() = 'Profile Hidden']").extract()
            if hidden:
                self.logger.warning('Profile hidden')
            else:
                self.logger.warning("Other error")
        headings = ['Tel', 'Fax', 'Address', 'Email', 'Website']
        for heading in headings:
            try:
                if heading in ["Email", "Website"]:
                    val = contacts.xpath(
                        "//strong[contains(text(),'%s')]/"
                        "following-sibling::a/text()" % heading).extract()[0].strip()
                else:
                    val = contacts.xpath(
                        "//strong[contains(text(),'%s')]/"
                        "following-sibling::text()[1]" % heading).extract()[0].strip()
            except IndexError:
                val = ""
            datum[heading.lower()] = val
        yield PracticeItem(**datum)
