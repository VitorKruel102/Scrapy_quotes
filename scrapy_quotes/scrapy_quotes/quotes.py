from scrapy import Request, Spider

URL = 'https://quotes.toscrape.com/'
class QuotesScrapy(Spider):
    """."""
    name = 'QuotesScrapy'

    def start_requests(self):
        return [Request(URL)]

    def parse(self, response):
        """."""
        self.log(f'Acessado o site {response.url}')
        quotes = response.xpath("*//div[@class='quote']")

        for quote in quotes:
            yield {
                'Title': quote.xpath('.//span[@class="text"]/text()').get(),
                'Author': quote.xpath('.//small[@class="author"]/text()').get(),
                'Tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()
            }
        
        next_pag = response.xpath("*//li[@class='next']/a/@href").get()

        if next_pag is not None:
            yield Request(response.urljoin(next_pag), callback=self.parse)
