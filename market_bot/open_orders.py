import requests
from bs4 import BeautifulSoup
from globals import base_path


def getOpenBuyOrdersList(data):
    buyOrders = []
    openOrdersPage = requests.get(base_path + "orders/buy_orders", headers=data)
    soup = BeautifulSoup(openOrdersPage.text, "html.parser")

    try:
        ordersList = soup.find("tbody")
        openOrder = ordersList.find_all("tr")
        for each in openOrder:
            playerDict = {}
            playerName = each.contents[3].text.strip()
            postedPrice = each.contents[5].text.strip().replace(",", "")
            orderID = each.get("id")
            playerURL = each.find("a")
            playerURL = (
                "https://mlb23.theshow.com" + playerURL["href"].lstrip().rstrip()
            )
            playerDict["Name"] = playerName
            playerDict["Posted Price"] = postedPrice
            playerDict["URL"] = playerURL
            playerDict["Order ID"] = orderID
            buyOrders.append(playerDict)

        return buyOrders
    except AttributeError:
        return buyOrders


def getOpenSellOrdersList(data):
    sellOrders = []
    try:
        openOrdersPage = requests.get(base_path + "orders/sell_orders", headers=data)
        soup = BeautifulSoup(openOrdersPage.text, "html.parser")
        ordersList = soup.find("tbody")
        openOrder = ordersList.find_all("tr")
        for each in openOrder:
            playerDict = {}
            playerName = each.contents[3].text.strip()
            postedPrice = each.contents[5].text.strip().replace(",", "")
            orderID = each.get("id")
            playerURL = each.find("a")
            playerURL = (
                "https://mlb23.theshow.com" + playerURL["href"].lstrip().rstrip()
            )
            playerDict["Name"] = playerName
            playerDict["Posted Price"] = postedPrice
            playerDict["URL"] = playerURL
            playerDict["Order ID"] = orderID
            sellOrders.append(playerDict)

        return sellOrders

    except AttributeError:
        return sellOrders


def getTotalOpenOrders(data):
    buyOrderList = getOpenBuyOrdersList(data)
    sellOrderList = getOpenSellOrdersList(data)
    return buyOrderList + sellOrderList
