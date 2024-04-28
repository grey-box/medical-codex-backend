import scrapy


class CompendiumSpider(scrapy.Spider):
    """
    Spider for Compendium
    """
    name = "compendium"
    start_urls = ['https://compendium.com.ua/akt/']

    def parse(self, response):
        """

        :param response:
        :return:
        """
        for alphabet_page in response.css("#site > div.container > div > main > div > ul > li > a"):
            url = response.urljoin(alphabet_page.css('::attr(href)').get())
            yield scrapy.Request(url, callback=self.parse_alphabet)

    def parse_alphabet(self, response):
        """

        :param response:
        :return:
        """
        for med_page in response.css("#site > div.container > div > main > div > div > div > a"):
            url = response.urljoin(med_page.css('::attr(href)').get())
            yield {
                'url': url,
                'title': med_page.css('::text').get()
            }
        for next_page in response.css("#site > div.container > div > main > nav > ul > li > a.next.page-link"):
            url = response.urljoin(next_page.css('::attr(href)').get())
            yield scrapy.Request(url, callback=self.parse_alphabet)
