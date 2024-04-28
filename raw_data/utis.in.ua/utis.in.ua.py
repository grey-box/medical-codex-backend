import scrapy


class MedsSpider(scrapy.Spider):
    name = "meds"
    start_urls = ['http://utis.in.ua/list']+['http://utis.in.ua/list'+str(i) for i in range(2, 22)]

    def parse(self, response):
        for url in response.css('#art-main > div > div > div > div > div.art-layout-cell.art-content > article.page > div > div > table > tbody > tr > td > ul > li > a'):
            yield {
                'url': response.urljoin(url.css('::attr(href)').get()),
                'title': url.css('::text').get(),
            }
