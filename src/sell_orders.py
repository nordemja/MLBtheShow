import requests
from bs4 import BeautifulSoup

from .captcha_solver import CaptchaSolver
from .auth_token import AuthToken


class SellOrders:
    def __init__(self, completed_orders_path, headers, browser):
        self.completed_orders_path = completed_orders_path
        self.headers = headers
        self.browser = browser

    def execute_sell_orders(self):
        print("Executing sell orders....")

        auth_token = AuthToken(player_url=None, headers=self.headers)

        # Fetch the list of sellable players from completed orders
        sellable_players = self._fetch_sellable_players()

        if sellable_players:
            # Once we have the players to sell, solve CAPTCHA and place orders
            captcha_solver = CaptchaSolver()
            captcha_solver.send_captcha_requests(sellable_players)

            auth_token.player_url = sellable_players["URL"]
            auth_token_list = auth_token.get_sell_auth_token()
            # get buy/sell amount
            captcha_tokens = captcha_solver.get_captcha_tokens(sellable_players)
            # place order

        print("DONE EXECUTING SELL ORDERS")
        return self.headers

    def _fetch_sellable_players(self):
        # This method fetches all completed orders and identifies which players are sellable
        attempts = 0
        while True:
            try:
                completed_page = requests.get(
                    self.completed_orders_path, headers=self.headers
                )
                soup = BeautifulSoup(completed_page.text, "html.parser")
                total_pages = int(
                    soup.find("div", {"class": "pagination"}).find("a").text
                )
                break
            except:
                attempts += 1
                if attempts >= 5:
                    self._refresh_session()
                    attempts = 0
        sell_players = []
        for page in range(1, total_pages + 1):
            print(f"PAGE: {page}")
            player_order_info = self._get_orders_from_page(page)
            if not player_order_info:
                break

            for row in player_order_info:
                try:
                    player_name = row.contents[1].text.strip()
                    order_type = row.contents[3].text.strip().split()[0]
                    if order_type == "Bought":
                        player_url = (
                            "https://mlb23.theshow.com" + row.find("a")["href"].strip()
                        )
                        # Check if the player is sellable
                        if getTotalSellable(player_url, self.headers) > 0:
                            sell_players.append(
                                {"player name": player_name, "URL": player_url}
                            )
                            print(player_name)
                except:
                    continue
        return sell_players

    def _get_orders_from_page(self, page):
        # Fetch orders for a specific page
        attempts = 0
        while True:
            try:
                resp = requests.get(
                    f"{self.completed_orders_path}?page={page}&", headers=self.headers
                )
                soup = BeautifulSoup(resp.text, "html.parser")
                return soup.find("tbody").find_all("tr")
            except:
                attempts += 1
                if attempts >= 5:
                    self._refresh_session()
                    return None
