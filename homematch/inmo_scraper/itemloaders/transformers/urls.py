import re
from typing import List


def extract_urls_from_html_with_re(
    text: str,
) -> List[str]:
    suffix: str = ".jpg"
    splitter: str = ","
    text_links = text.split(splitter)
    urls = [re.findall(rf"https?://[^\s]+{suffix}", link)[0] for link in text_links]

    return urls


def get_asset_operation_type(url: str) -> str:
    if "alquilar" in url:
        return "rental"
    if "comprar" in url:
        return "purchase"
    else:
        return None
