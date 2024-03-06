from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from homematch.inmo_scraper.itemloaders.transformers import strings


class CardPisosdotcomItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    url_in = MapCompose(lambda x: "https://www.pisos.com" + x)
    normalized_title_in = MapCompose(str.strip, str.lower, lambda x: x.replace(" ", "_"))
    subtitle_in = MapCompose(lambda x: x.strip())
    current_price_in = MapCompose(*strings.convert_price())
    drop_price_in = MapCompose(*strings.convert_price())
    # basic_info_in = Identity()
    ad_text_in = MapCompose(lambda x: x.strip())
    basic_info_out = Identity()
