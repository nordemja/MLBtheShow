import requests
from bs4 import BeautifulSoup


def get_total_sellable(playerURL, data):
    try:
        player_page = requests.get(playerURL, headers=data)
        soup = BeautifulSoup(player_page.text, "html.parser")
        total_sellable = soup.find_all("div", {"class": "well"})
        for each in total_sellable:
            if "Sellable" in each.text.strip():
                total_sellable = each.text.strip()[-1]
                return int(total_sellable)
    except Exception as e:
        print(e)
