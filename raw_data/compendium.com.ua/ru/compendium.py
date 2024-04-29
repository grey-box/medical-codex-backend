import scrapy
from scrapy.http import Response


class CompendiumSpider(scrapy.Spider):
    """
    Spider for Compendium
    """
    name = "compendium"
    start_urls = ['https://compendium.com.ua/akt/192/']

    def parse(self, response: Response):
        """
        :param response:
        :return:
        """

        for alphabet_page in response.css("#__layout > div > article > div.cp-agent-list__wrapper.cp-container > section.cp-agent-list__alphabet-wrapper.cp-alphabet-list-wrapper > div > ul > li > a"):
            url = response.urljoin(alphabet_page.css('::attr(href)').get())
            yield scrapy.Request(url, callback=self.parse_alphabet)

    def parse_alphabet(self, response):
        """
        :param response:
        :return:
        """

        for med_page in response.css("#__layout > div > article > div.cp-agent-list__wrapper.cp-container > section.cp-agent-list__list-item-wrapper > a"):
            url = response.urljoin(med_page.css('::attr(href)').get())
            yield {
                'url': url,
                'title': med_page.css('span.cp-agent-list__list-item-text::text').get()
            }

        for next_page in response.css("#__layout > div > article > div.cp-agent-list__wrapper.cp-container > div.cp-agent-list-paginator__wrapper.cp-container > div > div > a.cp-btn.cp-paginator__link.cp-paginator__link_next.cp-btn-light.cp-btn-sm.cp-btn-has-text"):
            url = response.urljoin(next_page.css('::attr(href)').get())
            yield scrapy.Request(url, callback=self.parse_alphabet)
