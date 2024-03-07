import lancedb
from datasets import Dataset

from homematch.config import DATA_DIR, TABLE_NAME
from homematch.data.types import ImageData


def datagen() -> list[ImageData]:
    dataset = Dataset.load_from_disk(DATA_DIR / "properties_dataset")

    # return Image instances
    return [ImageData(**batch) for batch in dataset]


def main() -> None:
    uri = str(DATA_DIR) + "/.lancedb/"
    db = lancedb.connect(uri)
    table = db.create_table(TABLE_NAME, schema=ImageData, exist_ok=True)
    data = datagen()
    table.add(data)


if __name__ == "__main__":
    main()
