import requests
import re
from bs4 import BeautifulSoup


class Stubs:
    def __init__(self, headers):
        self.headers = headers

    def get_stubs_amount(self, base_path):
        stubs_amount = requests.get(base_path, headers=self.headers)
        soup = BeautifulSoup(stubs_amount.text, "html.parser")
        stubs_amount = (
            soup.find("div", {"class": "well stubs"})
            .text.strip()
            .replace("Stubs Balance\n\n", "")
            .replace(",", "")
            .replace("Wallet\n", "")
        )
        return int(stubs_amount)
