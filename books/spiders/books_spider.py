from scrapy import Spider, Request
from books.items import BooksItem
import re
import math


class WhiskeySpider(Spider):
	name = 'books_spider'
	allowed_urls = ['https://www.goodreads.com/']
	start_urls = ['https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page=1']


	def parse(self, response):
		total_pages = int(response.xpath('//div[@class="pagination"]/a//text()').extract()[-2])

		page_urls = [f'https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page={i+1}' for i in range(total_pages)]

		for url in page_urls:
			yield Request(url=url, callback=self.parse_list_page)

	def parse_list_page(self, response):

		product_urls = response.xpath('//td[@width="100%"]/a/@href').extract()

		product_urls = [f'https://www.goodreads.com{url}' for url in product_urls]

		for url in product_urls:
			yield Request(url=url, callback=self.parse_review_page)

	def parse_review_page(self, response):


		Title = response.xpath('//div[@id="metacol"]/h1/text()').extract_first().strip()
		Author = response.xpath('//div[@class="authorName__container"]/a/span/text()').extract_first()
		Score = response.xpath('//div[@id="bookMeta"]/span/text()').extract_first().strip()
			
		Pages = response.xpath('//span[@itemprop="numberOfPages"]/text()').extract_first().strip()
		Pages = int(re.findall('\d+', Pages)[0])

		Genre = response.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()').extract()
		Year =str(response.xpath('//div[@class="row"]//text()').extract())
		Year = int(re.findall('((200|201)\d+)', Year)[0][0])



		item = BooksItem()
		item['Title'] = Title
		item['Author'] = Author
		item['Score'] = Score
		item['Pages'] = Pages
		item['Genre'] = Genre
		item['Year'] = Year

		yield item
