import hashlib
import io
import logging
from typing import List

import numpy as np
from lancedb.pydantic import LanceModel, vector
from PIL import Image
from pydantic import BaseModel, Field, computed_field

from homematch.config import IMAGES_DIR

logger = logging.getLogger(__name__)


class PropertyListingBase(BaseModel):
    page_source: str
    resource_title: str
    resource_country: str
    operation_type: str
    active: bool
    url: str
    title: str
    normalized_title: str
    zone: str
    current_price: float | None = None
    ad_text: str
    basic_info: List[str]
    last_update: str
    main_image_url: str
    scraped_ts: str

    @computed_field  # type: ignore
    @property
    def identificator(self) -> str:
        return hashlib.sha256(self.url.encode()).hexdigest()[:16]

    @computed_field  # type: ignore
    @property
    def text_description(self) -> str:
        basic_info_text = ",".join(self.basic_info)
        basic_info_text = basic_info_text.replace("habs", "bedrooms")
        basic_info_text = basic_info_text.replace("baños", "bathrooms")
        basic_info_text = basic_info_text.replace("baño", "bathroom")
        basic_info_text = basic_info_text.replace("m²", "square meters")
        basic_info_text = basic_info_text.replace("planta", "floor")
        basic_info_text = basic_info_text.replace("Bajo", "0 floor")

        description = ""
        description += f"Zone: {self.zone}."
        description += f"\nPrice: {self.current_price} euros."
        description += f"\nFeatures: {basic_info_text}"

        return description


class PropertyListing(PropertyListingBase):
    images_dir: str = Field(str(IMAGES_DIR), description="Directory to store images")

    @property
    def image_path(self) -> str:
        return str(self.images_dir) + f"/{self.identificator}.jpg"

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

    @classmethod
    def pil_to_numpy(cls, img: Image.Image) -> np.ndarray:
        return np.array(img)


class PropertyData(PropertyListing):
    class Config:
        arbitrary_types_allowed = True

    image: Image.Image


class ImageData(PropertyListing, LanceModel):
    vector: vector(768)  # type: ignore
    image_bytes: bytes
