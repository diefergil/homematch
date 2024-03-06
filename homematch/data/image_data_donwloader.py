import logging
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from pydantic import BaseModel

from homematch.config import IMAGES_DIR
from homematch.data.types import PropertyListingBase

logger = logging.getLogger(__name__)


class ImageDataDownloader(BaseModel):
    properties: list[PropertyListingBase]
    images_dir: Path | str = IMAGES_DIR
    quality: int = 75
    max_width: int = 224
    max_height: int = 224

    def save_images(self):
        for property in self.properties:
            image = self.get_image(property)
            if image:
                # Resize image if it exceeds max dimensions
                if image.width > self.max_width or image.height > self.max_height:
                    image.thumbnail((self.max_width, self.max_height))
                # Save image with specified quality
                image_path = Path(self.images_dir) / f"{property.identificator}.jpg"
                image_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(image_path, quality=self.quality)

    @staticmethod
    def get_image(property: PropertyListingBase) -> bytes:
        if property.main_image_url:
            url = property.main_image_url
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    image_content = response.content
                    image = Image.open(BytesIO(image_content))
                    return image
                else:
                    logger.error(f"Failed to download image for {property.title}")
            except requests.RequestException as e:
                logger.error(f"Error downloading image for {property.title}: {e}")
        return None
