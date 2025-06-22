import scrapy


class IllustDetailItem(scrapy.Item):
    illust_code = scrapy.Field()
    illust_type = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    thumbnail_url = scrapy.Field()
    tags = scrapy.Field()
    restrict = scrapy.Field()
    ai_type = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    page_count = scrapy.Field()
    like_count = scrapy.Field()
    bookmark_count = scrapy.Field()
    view_count = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    images = scrapy.Field()
    author = scrapy.Field()


class IllustImageItem(scrapy.Item):
    illust_code = scrapy.Field()
    mini_url = scrapy.Field()
    small_url = scrapy.Field()
    regular_url = scrapy.Field()
    original_url = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()


class AuthorItem(scrapy.Item):
    user_code = scrapy.Field()
    name = scrapy.Field()
    image_url = scrapy.Field()
