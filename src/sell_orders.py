import requests
from bs4 import BeautifulSoup

from .captcha_solver import CaptchaSolver


class SellOrders:
    def __init__(self, completed_orders_path, card_series_link, headers, browser):
        self.completed_orders_path = completed_orders_path
        self.card_series_link = card_series_link
        self.headers = headers
        self.browser = browser

    def execute(self):
        print("Executing sell orders....")

        # Fetch the list of sellable players from completed orders
        sellable_players = self._fetch_sellable_players()

        if sellable_players:
            print("\n")
            # Once we have the players to sell, solve CAPTCHA and place orders
            solver = CaptchaSolver(
                players=sellable_players,
                driver=self.browser,
                order_type="sell",
                headers=self.headers,
                double_check=False,
                card_series_link=self.card_series_link,
                browser=self.browser,
            )
            # Solve the CAPTCHA and place the orders
            self.headers = solver.solve()

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
