import requests
import re
from bs4 import BeautifulSoup
from globals import base_path


def get_stubs_amount(data):
    stubs_amount = requests.get(base_path + "dashboard", headers=data)
    soup = BeautifulSoup(stubs_amount.text, "html.parser")
    stubs_amount = (
        soup.find("div", {"class": "well stubs"})
        .text.strip()
        .replace("Stubs Balance\n\n", "")
        .replace(",", "")
        .replace("Wallet\n", "")
    )
    return int(stubs_amount)


def get_buy_amount(playerURL, data):
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
    returnval = min(amount_lst)
    return returnval


def get_sell_amount(playerURL, data):
    amount_lst = []
    x = requests.get(playerURL, headers=data)
    soup = BeautifulSoup(x.text, "html.parser")
    sell_amount = soup.find_all("input", {"name": "price"})
    for x in sell_amount:
        val = str(x).split(" ")[-1]
        prop = val.split("=")
        if prop[0] == "value":
            amount = int(re.findall(r'"([^"]*)"', prop[1])[0])
            amount_lst.append(amount)
    return_val = max(amount_lst)
    return return_val
