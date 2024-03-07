import datetime

import scrapy
from scrapy.selector import Selector

from homematch.config import SCRAPER_URLS
from homematch.inmo_scraper.itemloaders.pisosdotcom import CardPisosdotcomItemLoader
from homematch.inmo_scraper.items import PropertyCard


class PisosdotcomSpider(scrapy.Spider):
    name = "pisosdotcom"
    allowed_domains = ["pisos.com"]
    start_urls = start_urls_base = SCRAPER_URLS

    start_urls = [url + "/fecharecientedesde-desc/" for url in start_urls_base]

    custom_settings = {
        "stop_condition": "Hace más de 1 mes",
    }

    _stop_following_links = False

    def parse(self, response):
        self.current_start_url = response.url
        if self._stop_following_links:
            self.logger.info(f"Stopping spider at URL {response.url}")
            self._stop_following_links = False
            return
        flats = response.xpath('//div[@class="ad-preview    ad-preview--has-desc "]')
        for flat_index, flat in enumerate(flats):
            yield self.extract_info_from_flat(flat)

        # pass next page when the first one is finished
        self.next_page = response.xpath(
            '//div[@class="pagination__next blue-border single"]/a/@href'
        ).extract_first()

        if not self.next_page:
            self.next_page = response.xpath(
                '//div[@class="pagination__next border-l"]/a/@href'
            ).extract_first()

        if self.next_page:
            # next_page_url = response.urljoin(next_page_id)
            yield response.follow(self.next_page, callback=self.parse)

    def extract_info_from_flat(self, flat: scrapy.selector.unified.Selector):
        property = CardPisosdotcomItemLoader(item=PropertyCard(), selector=flat)

        property.add_value("page_source", self.current_start_url)
        property.add_value("resource_title", "pisos.com")
        property.add_value("resource_country", "ES")
        property.add_css("operation_type", "div.ad-preview::attr(data-lnk-href)")

        # Property
        property.add_value("active", True)
        property.add_css("url", "div.ad-preview::attr(data-lnk-href)")
        property.add_css("title", "a.ad-preview__title::text")
        property.add_css("normalized_title", "a.ad-preview__title::text")
        property.add_css("zone", "p.p-sm::text")

        # # Price
        property.add_css("current_price", "span.ad-preview__price::text", re="(.+) €")
        property.add_css("drop_price", "span.ad-preview__drop::text", re="(.+) €")
        property.add_css(
            "percentage_drop_price", "span.ad-preview__drop::text", re="(\d+)?%"
        )

        property.add_css("ad_text", "p.ad-preview__description::text")
        property.add_css("basic_info", "p.ad-preview__char.p-sm::text")
        property.add_css(
            "last_update",
            "span.ad-preview__product-tag.ad-preview__product-tag--date::text",
        )

        # multimedia
        carousel_slides = property.get_css(
            ".carousel__slide:not(.carousel__hidden):not(.u-hide)"
        )
        main_image_url = None

        for slide_html in carousel_slides:
            slide_selector = Selector(text=slide_html)
            # Check for 'src' attribute first
            img_src = slide_selector.css("img::attr(src)").get()
            # If 'src' is not found, check for 'data-src'
            if not img_src:
                img_src = slide_selector.css("img::attr(data-src)").get()
            # If an image source is found, set it as the main image URL and break the loop
            if img_src:
                main_image_url = img_src
                break

        property.add_value("main_image_url", main_image_url)

        # metadata
        property.add_value(
            "scraped_ts", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        last_update = property.get_css(
            "span.ad-preview__product-tag.ad-preview__product-tag--date::text"
        )[-1]

        self.set_stop_contition(last_update)

        return property.load_item()

    def set_stop_contition(self, last_update):
        if last_update == self.custom_settings.get("stop_condition"):
            self._stop_following_links = True


if __name__ == "__main__":
    import os
    import pathlib

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
    os.chdir(CURRENT_PATH)
    process = CrawlerProcess(get_project_settings())
    process.crawl("pisosdotcom")
    process.start()
