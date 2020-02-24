import scrapy


class Post(scrapy.Item):
    post_id = scrapy.Field()
    available = scrapy.Field()
    creator_id = scrapy.Field()
    language = scrapy.Field()
    first_published_at = scrapy.Field()
    title = scrapy.Field()
    word_count = scrapy.Field()
    claps = scrapy.Field()
    tags = scrapy.Field()
    paragraphs = scrapy.Field()


class Paragraph(scrapy.Item):
    index = scrapy.Field()
    name = scrapy.Field()
    type_ = scrapy.Field()
    text = scrapy.Field()
