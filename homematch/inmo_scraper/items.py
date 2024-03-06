# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertyCard(scrapy.Item):
    # Resource
    page_source = scrapy.Field(default=None)
    resource_title = scrapy.Field(default=None)
    resource_country = scrapy.Field(default=None)
    operation_type = scrapy.Field(default=None)

    # Property
    active = scrapy.Field(default=None)
    url = scrapy.Field(default=None)
    title = scrapy.Field(default=None)
    normalized_title = scrapy.Field(default=None)
    subtitle = scrapy.Field(default=None)
    zone = scrapy.Field(default=None)

    # Price
    current_price = scrapy.Field(default=None)
    drop_price = scrapy.Field(default=None)
    percentage_drop_price = scrapy.Field(default=None)

    # Details
    ad_text = scrapy.Field(default=None)
    basic_info = scrapy.Field(default=None)
    last_update = scrapy.Field(default=None)

    # Multimedia
    main_image_url = scrapy.Field(default=None)

    # Additional
    published = scrapy.Field(default=None)
    scraped_ts = scrapy.Field(default=None)

    # DB
    insert_timestamp = scrapy.Field(default=None)
    update_timestamp = scrapy.Field(default=None)
    pipeline_ts = scrapy.Field(default=None)
