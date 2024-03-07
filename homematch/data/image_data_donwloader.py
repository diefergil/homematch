import logging
import os
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
    images_dir: Path = IMAGES_DIR
    quality: int = 75
    max_width: int = 224
    max_height: int = 224
    success_request_code: int = 200

    @property
    def images_downloaded(self) -> list[str]:
        images_files = os.listdir(self.images_dir)
        return [
            os.path.splitext(image_file)[0]
            for image_file in images_files
            if image_file.endswith(".jpg")
        ]

    def save_images(self, force: bool = False, resize_images: bool = True) -> None:
        for home_property in self.properties:
            if force or home_property.identificator not in self.images_downloaded:
                image = self.get_image(home_property)
                if image:
                    # Resize image
                    image = self.resize_image(
                        image, width=self.max_width, height=self.max_height
                    )
                    if image:
                        # Save image with specified quality
                        image_path = Path.joinpath(
                            self.images_dir, f"{home_property.identificator}.jpg"
                        )
                        image_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(image_path, "wb") as file:
                            image.save(file, format="JPEG", quality=self.quality)

    def get_image(self, home_property: PropertyListingBase) -> Image.Image | None:
        if home_property.main_image_url:
            url = home_property.main_image_url
            try:
                response = requests.get(url, stream=True)
                if response.status_code == self.success_request_code:
                    image_content = response.content
                    image = Image.open(BytesIO(image_content))
                    return image
                else:
                    logger.error(f"Failed to download image for {home_property.title}")
            except requests.RequestException as e:
                logger.error(f"Error downloading image for {home_property.title}: {e}")
        return None

    @staticmethod
    def resize_image(image: Image.Image, width: int, height: int) -> Image.Image | None:
        image = image.convert("RGB")  # Convert RGBA to RGB
        if image.width > width or image.height > height:
            image.thumbnail((width, height))
            return image
        return None
