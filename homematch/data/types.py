import hashlib
import io
import logging
from pathlib import Path
from typing import List

from PIL import Image
from pydantic import BaseModel, Field, HttpUrl, computed_field

from homematch.config import IMAGES_DIR

logger = logging.getLogger(__name__)


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


class PropertyListing(PropertyListingBase):
    images_dir: Path = Field(IMAGES_DIR, description="Directory to store images")

    @property
    def image_path(self) -> Path:
        return self.images_dir / f"{self.identificator}.jpg"

    def load_image(self) -> Image.Image:
        try:
            return Image.open(self.image_path)
        except FileNotFoundError:
            logger.error(f"Image file not found: {self.image_path}")
            raise

    @classmethod
    def pil_to_bytes(cls, img: Image.Image) -> bytes:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()


class PropertyData(PropertyListing):
    image_bytes: bytes

    def to_pil(self):  # type: ignore
        return Image.open(io.BytesIO(self.image))
