import requests
from bs4 import BeautifulSoup

def getBuyAuthToken(playerURL, data):
    buyAuthList = []
    pageRequest = requests.get(playerURL, headers= data)
    soup = BeautifulSoup(pageRequest.text, 'html.parser')
    buyForm = soup.find_all('input', {'name': 'authenticity_token'})
    for each in buyForm:
        buyAuthList.append(each.get('value'))
    return buyAuthList

def getSellAuthToken(playerURL, data):
    sellAuthList = []
    pageRequest = requests.get(playerURL, headers= data)
    soup = BeautifulSoup(pageRequest.text, 'html.parser')
    sellForm = soup.find_all('input', {'name': 'authenticity_token'})
    for each in sellForm:
        sellAuthList.append(each.get('value'))
    return sellAuthList