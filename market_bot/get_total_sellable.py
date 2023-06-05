import requests
from bs4 import BeautifulSoup


def getTotalSellable(playerURL, data):
    try:
        playerPage = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(playerPage.text, 'html.parser')
        totalSellable = soup.find_all('div', {'class': 'well'})[4].text.strip()[-1]
        return int(totalSellable)
    except Exception as e:
        print(e)