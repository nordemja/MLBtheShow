import requests
from bs4 import BeautifulSoup


class Token:
    def __init__(self, player_url, headers):
        self.player_url = player_url
        self.headers = headers

    def get_sell_auth_token():
        sell_auth_list = []
        page_request = requests.get(player_url=self.player_url, headers=self.headers)
        soup = BeautifulSoup(page_request.text, "html.parser")

        sell_form = soup.find_all("input", {"name": "authenticity_token"})
        for each in sell_form:
            auth_token_list.append(each.get("value"))
        return auth_token_list

    def get_buy_auth_token():
        buy_auth_list = []
        page_request = requests.get(self.player_url, headers=self.headers)
        soup = BeautifulSoup(page_request.text, "html.parser")
        buy_form = soup.find_all("input", {"name": "authenticity_token"})
        for each in buy_form:
            auth_token_list.append(each.get("value"))
        return auth_token_list


# def get_buy_auth_token(playerURL, data):
#     buy_auth_list = []
#     page_request = requests.get(playerURL, headers=data)
#     soup = BeautifulSoup(page_request.text, "html.parser")
#     buy_form = soup.find_all("input", {"name": "authenticity_token"})
#     for each in buy_form:
#         buy_auth_list.append(each.get("value"))
#     return buy_auth_list


# def get_sell_auth_token(playerURL, data):
#     sell_auth_list = []
#     page_request = requests.get(playerURL, headers=data)
#     soup = BeautifulSoup(page_request.text, "html.parser")
#     sell_form = soup.find_all("input", {"name": "authenticity_token"})
#     for each in sell_form:
#         sell_auth_list.append(each.get("value"))
#     return sell_auth_list
