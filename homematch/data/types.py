import hashlib
from typing import List

from pydantic import BaseModel, HttpUrl, computed_field


class PropertyListingBase(BaseModel):
    page_source: HttpUrl
    resource_title: str
    resource_country: str
    operation_type: str
    active: bool
    url: HttpUrl
    title: str
    normalized_title: str
    zone: str
    current_price: float | None = None
    ad_text: str
    basic_info: List[str]
    last_update: str
    main_image_url: HttpUrl
    scraped_ts: str

    @computed_field  # type: ignore
    @property
    def identificator(self) -> str:
        return hashlib.sha256(self.url.unicode_string().encode()).hexdigest()[:8]
