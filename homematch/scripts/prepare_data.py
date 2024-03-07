import logging

import pandas as pd
from datasets import Dataset
from PIL import UnidentifiedImageError

from homematch.config import DATA_DIR
from homematch.data.crawler_data_loader import CrawlerDataLoader
from homematch.data.image_data_donwloader import ImageDataDownloader
from homematch.data.types import PropertyData, PropertyListing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    # Load property listing data from JSON
    logger.info("Loading property listing data...")
    crawler_data_loader = CrawlerDataLoader(file_name="fotocasa_flats.json")
    properties_listing_data = crawler_data_loader.load_from_json()

    # Download and save property images
    logger.info("Downloading property images...")
    image_data_downloader = ImageDataDownloader(properties=properties_listing_data)
    image_data_downloader.save_images()

    # Convert property listing data to PropertyListing objects
    logger.info("Converting property listing data to objects...")
    property_listing_list = [
        PropertyListing(**data.dict()) for data in properties_listing_data
    ]

    # Extract property data and handle image loading errors
    logger.info("Extracting property data...")
    properties_data = []
    for property_listing in property_listing_list:
        try:
            image_bytes = PropertyListing.pil_to_bytes(property_listing.load_image())
            property_data = PropertyData(
                **property_listing.dict(), image_bytes=image_bytes
            )
            properties_data.append(property_data)
        except UnidentifiedImageError as e:
            logger.error(f"Problem with image for {property_listing.title}: {e}")

    # Convert property data to pandas DataFrame
    logger.info("Converting property data to DataFrame...")
    df = pd.json_normalize(
        property_data.dict() for property_data in properties_data
    ).astype(
        {
            "page_source": str,
            "main_image_url": str,
            "url": str,
            "images_dir": str,
        }
    )
    logger.info(f"Dataset created successfully with {len(df)} rows")

    # Convert pandas DataFrame to Hugging Face Dataset
    logger.info("Converting DataFrame to Hugging Face Dataset...")
    dataset = Dataset.from_pandas(df)

    # Save dataset
    dataset_path = DATA_DIR / "properties_dataset"
    logger.info(f"Saving dataset to disk: {dataset_path}")
    dataset.save_to_disk(dataset_path)


if __name__ == "__main__":
    main()
