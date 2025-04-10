import requests
from bs4 import BeautifulSoup
from time import sleep


class Market:
    def __init__(self, card_series_link, headers, browser):
        self.headers = headers
        self.browser = browser
        self.card_series_link = card_series_link
        self.total_pages_found = 0

    def fetch_total_pages(self):
        card_series = requests.get(self.card_series_link, headers=self.headers)
        soup = BeautifulSoup(card_series.text, "html.parser")
        total_pages_found = int(soup.find("h3").text.strip()[-1])
        return total_pages_found

    def fetch_listings(self, page):
        search_reults = requests.get(
            f"{base_path}/community_market?page={page}&{self.card_series_link}",
            headers=self.headers,
        )
        soup = BeautifulSoup(search_reults.text, "html.parser")
        table = soup.find("tbody")
        return table.find_all("tr")
