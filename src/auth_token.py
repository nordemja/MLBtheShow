import requests
from bs4 import BeautifulSoup


class AuthToken:
    def __init__(self, headers):
        self.headers = headers

    def get_auth_tokens(self, player_list):
        for player in player_list:
            auth_token_list = []
            response = requests.get(player["URL"], headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            form_tags = soup.find_all("input", {"name": "authenticity_token"})
            for tag in form_tags:
                auth_token_list.append(tag.get("value"))

            player["auth_token_list"] = auth_token_list
