from homematch.data.crawler_data_loader import CrawlerDataLoader
from homematch.data.image_data_donwloader import ImageDataDownloader

crawler_data_loader = CrawlerDataLoader(file_name="fotocasa_flats.json")
data = crawler_data_loader.load_from_json()
image_data_downloader = ImageDataDownloader(properties=data)
image_data_downloader.save_images()
