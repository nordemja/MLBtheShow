import requests
from bs4 import BeautifulSoup


def getTotalSellable(playerURL, data):
    try:
        playerPage = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(playerPage.text, 'html.parser')
        totalSellable = soup.find_all('div', {'class': 'well'})
        for each in totalSellable:
            if "Sellable" in each.text.strip():
                totalSellable = each.text.strip()[-1]
                return int(totalSellable)
    except Exception as e:
        print(e)