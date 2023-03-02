import requests
from parsel import Selector


def get_html(url: str) -> Selector:
    response = requests.get(url)
    if response.status_code == 200:
        return Selector(response.text)
