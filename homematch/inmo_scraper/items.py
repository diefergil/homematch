# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertyCard(scrapy.Item):
    # Resource
    page_source = scrapy.Field()
    resource_title = scrapy.Field()
    resource_country = scrapy.Field()
    operation_type = scrapy.Field()

    # Property
    active = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    zone = scrapy.Field()

    # Price
    current_price = scrapy.Field()
    drop_price = scrapy.Field()
    percentage_drop_price = scrapy.Field()

    # Details
    ad_text = scrapy.Field()
    basic_info = scrapy.Field()
    last_update = scrapy.Field()

    # Multimedia
    main_image_url = scrapy.Field()

    # Additional
    published = scrapy.Field()
    scraped_ts = scrapy.Field()

    # DB
    insert_timestamp = scrapy.Field()
    update_timestamp = scrapy.Field()
    pipeline_ts = scrapy.Field()
