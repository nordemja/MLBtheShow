import requests
import re
from bs4 import BeautifulSoup
from globals import base_path

def getStubsAmount(data):
    stubsAmount = requests.get(base_path + 'dashboard', headers= data)
    soup = BeautifulSoup(stubsAmount.text, 'html.parser')
    stubsAmount = soup.find('div', {'class': 'well stubs'}).text.strip().replace('Stubs Balance\n\n', '').replace(',','').replace('Wallet\n','')
    return int(stubsAmount)

def getBuyAmount(playerURL, data):
    amount_lst = []
    x = requests.get(playerURL, headers= data)
    soup = BeautifulSoup(x.text, 'html.parser')
    buyAmountNew = soup.find_all('input', {'name': 'price'})
    for x in buyAmountNew:
        val = str(x).split(" ")[-1]
        prop = val.split("=")
        if prop[0] == "value":
            amount = int(re.findall(r'"([^"]*)"', prop[1])[0])
            amount_lst.append(amount)
    returnval = min(amount_lst)
    return returnval

def getSellAmount(playerURL, data):
    amount_lst = []
    x = requests.get(playerURL, headers= data)
    soup = BeautifulSoup(x.text, 'html.parser')
    sellAmount = soup.find_all('input', {'name': 'price'})
    for x in sellAmount:
        val = str(x).split(" ")[-1]
        prop = val.split("=")
        if prop[0] == "value":
            amount = int(re.findall(r'"([^"]*)"', prop[1])[0])
            amount_lst.append(amount)
    returnval = max(amount_lst)
    return returnval