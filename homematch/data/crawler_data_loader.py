import json
from pathlib import Path
from typing import List

from pydantic import BaseModel

from homematch.config import CRAWLER_DATA_DIR
from homematch.data.types import PropertyListingBase


class CrawlerDataLoader(BaseModel):
    data_dir: Path | str = CRAWLER_DATA_DIR
    file_name: str

    def load_from_json(self) -> List[PropertyListingBase]:
        file_path = Path(self.data_dir) / self.file_name
        with open(file_path, "r") as file:
            json_data = json.load(file)
        return [PropertyListingBase(**item) for item in json_data]
