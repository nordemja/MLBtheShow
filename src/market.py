import requests
from bs4 import BeautifulSoup
from stubs import Stubs
from headers import get_headers
from time import sleep


class Market:
    def __init__(self, headers, browser):
        self.headers = headers

    def fetch_total_pages(self):
        soup = BeautifulSoup(card_series.text, "html.parser")
        total_pages_found = int(soup.find("h3").text.strip()[-1])
