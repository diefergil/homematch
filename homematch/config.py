import pathlib

# Directories
PACKAGE_ROOT = pathlib.Path(__file__).parent.parent.resolve()
LOGS_DIR = pathlib.Path(PACKAGE_ROOT, "logs")
DATA_DIR = pathlib.Path(PACKAGE_ROOT, "data")
CRAWLER_DATA_DIR = pathlib.Path(DATA_DIR, "crawler_data")
IMAGES_DIR = pathlib.Path(DATA_DIR, "images")
