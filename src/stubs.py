import requests
import re
from bs4 import BeautifulSoup


class Stubs:
    def __init__(self, base_path, headers):
        self.base_path = base_path
        self.headers = headers

    def get_stubs_amount(self):
        stubs_amount = requests.get(self.base_path, headers=self.headers)
        soup = BeautifulSoup(stubs_amount.text, "html.parser")
        stubs_amount = (
            soup.find("div", {"class": "well stubs"})
            .text.strip()
            .replace("Stubs Balance\n\n", "")
            .replace(",", "")
            .replace("Wallet\n", "")
        )
        return int(stubs_amount)

    def get_order_amount(self, playerURL, order_flag):
        amount_lst = []
        x = requests.get(playerURL, headers=data)
        soup = BeautifulSoup(x.text, "html.parser")
        buy_amount_new = soup.find_all("input", {"name": "price"})
        for x in buy_amount_new:
            val = str(x).split(" ")[-1]
            prop = val.split("=")
            if prop[0] == "value":
                amount = int(re.findall(r'"([^"]*)"', prop[1])[0])
                amount_lst.append(amount)
        if order_flag == "buy":
            return max(amount_lst)
        return min(amount_lst)
