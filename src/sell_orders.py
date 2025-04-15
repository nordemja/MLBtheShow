import requests
from bs4 import BeautifulSoup

from .captcha_solver import CaptchaSolver
from .auth_token import AuthToken


class SellOrders:
    def __init__(self, single_item_api_path, completed_orders_path, headers, browser):
        self.single_item_api_path = single_item_api_path
        self.completed_orders_path = completed_orders_path
        self.headers = headers
        self.driver = browser.driver

    def execute_sell_orders(self):
        print("Executing sell orders....")

        sellable_players = self._fetch_sellable_players()

        if sellable_players:
            # Once we have the players to sell, solve CAPTCHA and place orders
            auth_token = AuthToken(headers=self.headers)
            captcha_solver = CaptchaSolver()
            captcha_solver.send_captcha_requests(sellable_players)
            auth_token.get_auth_tokens(sellable_players)
            self._get_item_sell_price(sellable_players)

            sellable_players_with_captcha_tokens = captcha_solver.get_captcha_tokens(
                sellable_players
            )
            self._place_sell_orders(sellable_players_with_captcha_tokens)

            print("DONE EXECUTING SELL ORDERS")

        return self.headers

    def _fetch_sellable_players(self):
        # This method fetches all completed orders and identifies which players are sellable
        completed_page = requests.get(self.completed_orders_path, headers=self.headers)
        soup = BeautifulSoup(completed_page.text, "html.parser")
        total_pages = int(soup.find("div", {"class": "pagination"}).find("a").text)

        sell_players = []
        for page in range(1, total_pages + 1):
            print(f"PAGE: {page}")
            player_order_info = self._get_orders_from_page(page)
            if not player_order_info:
                break

            for row in player_order_info:
                player_name = row.contents[1].text.strip()
                order_type = row.contents[3].text.strip().split()[0]
                if order_type == "Bought":
                    player_url = (
                        "https://mlb23.theshow.com" + row.find("a")["href"].strip()
                    )
                    # Check if the player is sellable
                    if self._get_total_sellable(player_url, self.headers) > 0:
                        uuid = player_url.split("/")[-1]
                        sell_players.append(
                            {
                                "player name": player_name,
                                "URL": player_url,
                                "uuid": uuid,
                            }
                        )
                        print(player_name)
                    else:
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

    def _get_total_sellable(self, playerURL, headers):
        try:
            player_page = requests.get(playerURL, headers=headers)
            soup = BeautifulSoup(player_page.text, "html.parser")
            total_sellable = soup.find_all("div", {"class": "well"})
            for each in total_sellable:
                if "Sellable" in each.text.strip():
                    total_sellable = each.text.strip()[-1]
                    return int(total_sellable)
        except Exception as e:
            print(e)

    def _get_item_sell_price(self, player_list):
        for player in player_list:
            response = requests.get(
                f"{self.single_item_api_path}?uuid={player['uuid']}"
            ).json()
            player["sell_price"] = response["best_sell_price"]

    def _place_sell_orders(self, player_list):
        for player in player_list:
            sellable_before = self._get_total_sellable(
                playerURL=player["URL"], headers=self.headers
            )
            self._inject_captcha_token_into_webpage(
                player_url=player["URL"], form_token=player["form_token"]
            )
            self._sell_order_post_request(
                player_url=player["URL"],
                sell_amount=player["sell_price"],
                form_token=player["form_token"],
                auth_token_list=player["auth_token_list"],
                sellable_before=sellable_before,
            )

    def _inject_captcha_token_into_webpage(self, player_url, form_token):
        self.driver.get(player_url)
        wirte_tokon_js = (
            f'document.getElementById("g-recaptcha-response").innerHTML="{form_token}";'
        )
        self.driver.execute_script(wirte_tokon_js)

    def _sell_order_post_request(
        self, player_url, sell_amount, form_token, auth_token_list, sellable_before
    ):
        for token in auth_token_list:
            form_data = {
                "authenticity_token": token,
                "price": sell_amount - 25,
                "g-recaptcha-response": form_token,
            }
            send_post = requests.post(
                player_url + "/create_sell_order", form_data, headers=self.headers
            )

        sellable_after = self._get_total_sellable(
            playerURL=player_url, headers=self.headers
        )

        if sellable_after != sellable_before:
            print(sellable_after)
            print(send_post)

        else:
            print(sellable_after)
            print("ORDER NOT PLACED")
