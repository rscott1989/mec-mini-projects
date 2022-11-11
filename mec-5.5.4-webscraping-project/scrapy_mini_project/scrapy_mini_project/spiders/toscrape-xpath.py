import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            tags = quote.xpath(".//div[@class='tags']//a/text()").extract()
            final_tag = [tag.strip() for tag in tags]
            yield {
                'text': quote.xpath(".//span[@class='text']/text()").extract_first().strip(),
                'author': quote.xpath(".//small[@class='author']/text()").extract_first().strip(),
                'tags': final_tag
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)