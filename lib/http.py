import random
import time
import uuid

import requests
from parsel import Selector


# def get_ip():
#     return ".".join(map(str, (random.randint(0, 255) for i in range(4))))


def get_html(url: str) -> Selector:
    response = requests.get(url, headers={
        "Referer": "https://www.kuaishuku.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

    })

    if response.status_code == 200:
        # print(response.text)
        return Selector(response.text)
