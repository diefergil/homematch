# Homematach

## Installation

```bash
poetry install
```

## How to use

1. Select a url from fotocasa.com, for example [this](https://www.pisos.com/viviendas/alicante_alacant/)
2. Modify in the config file, the var `SCRAPER_URLS`:

    ```python
        SCRAPER_URLS=[https://www.pisos.com/viviendas/alicante_alacant/]
    ```

3. Run the scraper with make:

    ```bash
    make crawl_landing_pisos
    ```

    A new json file will be created located in data/crawler_data

4. Run `scripts/prepare_data.py` to create the dataset.
5. Run `scripts/populate_database.py` to load the data in lance vector database
6. Run the app and query your data!
![Example](./assets/example.png)
