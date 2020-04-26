# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
	Title = scrapy.Field()
	Author = scrapy.Field()
	Score = scrapy.Field()
	Pages = scrapy.Field()
	Genre = scrapy.Field()
	Year = scrapy.Field()
	
