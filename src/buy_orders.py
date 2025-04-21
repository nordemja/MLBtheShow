import requests

from .captcha_solver import CaptchaSolver
from .auth_token import AuthToken
from .stubs import Stubs


class BuyOrders:
    def __init__(
        self,
        base_path,
        listings,
        open_orders,
        buy_order_length,
        total_open_listing_length,
        headers,
        browser,
        max_buy_orders=10,
        max_total_listings=25,
    ):
        self.base_path = base_path
        self.listings = listings
        self.open_orders = open_orders
        self.buy_order_length = buy_order_length
        self.total_open_listing_length = total_open_listing_length
        self.headers = headers
        self.driver = browser.driver
        self.max_buy_orders = max_buy_orders
        self.max_total_listings = max_total_listings
        self.stubs = Stubs(self.headers)

    def execute_buy_orders(self, players_to_buy: list[dict]):
        print("Executing buy orders....")

        if players_to_buy:
            # Once we have the players to buy, solve CAPTCHA and place orders
            auth_token = AuthToken(headers=self.headers)
            captcha_solver = CaptchaSolver()
            captcha_solver.send_captcha_requests(players_to_buy)
            auth_token.get_auth_tokens(players_to_buy)
            self._get_item_buy_price(player_list=players_to_buy)

            players_to_buy_with_captcha_tokens = captcha_solver.get_captcha_tokens(
                players_to_buy
            )

            self._place_buy_orders(players_to_buy_with_captcha_tokens)
            print("DONE PLACING BUY ORDERS")

        return self.headers

    def select_players(self):

        players_to_buy = []

        for listing in self.listings:
            name = listing["player name"]

            if self._is_order_placed(name):
                print(f"{name} already has an open order and is awaiting fufillment")
                continue

            if not self._check_listing_lengths():
                print("Maximum listing length reached!")
                print(f"Buy Orders Length: {self.buy_order_length}")
                print(f"Total Buy/Sell Orders Length: {self.total_open_listing_length}")
                break

            print(listing)
            players_to_buy.append(listing)
            self.buy_order_length += 1
            self.total_open_listing_length += 1

        return players_to_buy

    def _is_order_placed(self, player_name):
        return any(order["Name"] == player_name for order in self.open_orders)

    def _check_listing_lengths(self):
        return (
            self.buy_order_length < self.max_buy_orders
            and self.total_open_listing_length < self.max_total_listings
        )

    def _get_item_buy_price(self, player_list):
        for player in player_list:
            response = requests.get(
                f"{self.single_item_api_path}?uuid={player['uuid']}"
            ).json()
            player["buy amount"] = response["best_buy_price"]

    def _place_buy_orders(self, player_list):
        for player in player_list:
            self._inject_captcha_token_into_webpage(
                player_url=player["URL"], form_token=player["form_token"]
            )
            self._buy_order_post_request(
                player_url=player["URL"],
                buy_amount=player["buy amount"],
                form_token=player["form_token"],
                auth_token_list=player["auth_token_list"],
            )

    def _inject_captcha_token_into_webpage(self, player_url, form_token):
        self.driver.get(player_url)
        wirte_tokon_js = (
            f'document.getElementById("g-recaptcha-response").innerHTML="{form_token}";'
        )
        self.driver.execute_script(wirte_tokon_js)

    def _buy_order_post_request(
        self, player_url, buy_amount, form_token, auth_token_list
    ):

        stubs_before = self.stubs.get_stubs_amount(self.base_path)

        for each in auth_token_list:
            form_data = {
                "authenticity_token": each,
                "price": buy_amount + 25,
                "g-recaptcha-response": form_token,
            }
            send_post = requests.post(
                f"{player_url}/create_buy_order", form_data, headers=self.headers
            )

        stubs_after = self.stubs.get_stubs_amount(self.base_path)
        if stubs_before != stubs_after:
            # print('i = ' + str(authToken.index(each)))
            # print("length of authToken = " +str(len(authToken)))
            print(send_post)

        else:
            print("ORDER NOT PLACED")
