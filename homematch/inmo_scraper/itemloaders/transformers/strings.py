import re


def extract_numers(string: str) -> int:
    return re.findall(r"\b\d+\b", string)


def strip_string(string: str) -> str:
    return string.strip()


def clean_dots(string: str) -> str:
    return string.replace(".", "")


def remove_puntuaction(string):
    return "".join(e for e in string if e.isalnum())


def convert_price():
    return [strip_string, clean_dots, extract_numers, float]
