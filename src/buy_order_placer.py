import requests

from config.globals import BUY_ORDER_OVERBID

from .captcha_solver import CaptchaSolver
from .auth_token import AuthToken
from .stubs import Stubs


class BuyOrderPlacer:
    """
    Handles logic related to selecting players to buy, solving CAPTCHAs,
    obtaining auth tokens, and placing buy orders on a platform.

    Attributes:
        single_item_api_path (str): API endpoint used to retrieve item pricing information.
        headers (dict): Headers used for authenticated HTTP requests.
        driver (BrowserSession.driver): Selenium browser driver used to inject CAPTCHA tokens.
        stubs (Stubs): Utility class instance for managing and checking stubs balance.

    Methods:
        execute_buy_orders(players_to_buy: list[dict]) -> dict:
            Coordinates CAPTCHA solving, token retrieval, price updates, and order placement.

        _get_item_buy_price(player_list: list[dict]) -> None:
            Retrieves and sets the best current buy price for each player.

        _place_buy_orders(player_list: list[dict]) -> None:
            Performs the final order placement logic for each player.

        _inject_captcha_token_into_webpage(player_url: str, form_token: str) -> None:
            Injects CAPTCHA token directly into the player's web page using the browser.

        _buy_order_post_request(
            player_url: str, buy_amount: float, form_token: str, auth_token_list: list
        ) -> None:
            Submits a POST request to create a buy order with CAPTCHA and auth tokens.
    """

    def __init__(
        self,
        single_item_api_path,
        headers_instance,
        browser,
    ):
        """
        Initialize the BuyOrders object.

        Args:
            single_item_api_path (str): API endpoint for fetching single item data.
            headers (dict): Headers used for authenticated HTTP requests.
            browser (BrowserSession): Browser session object containing the Selenium driver.
        """
        self.single_item_api_path = single_item_api_path
        self.headers_instance = headers_instance
        self.driver = browser.driver
        self.stubs = Stubs(self.headers_instance)
        self.active_headers = None

    def execute_buy_orders(self, players_to_buy: list[dict]):
        """
        Handles the full flow for placing buy orders including:
        CAPTCHA solving, auth token extraction, and making the order.

        Args:
            players_to_buy (list): List of players selected for purchase.

        Returns:
            dict: Headers used during the requests, potentially reused externally.
        """
        print("Executing buy orders....")

        if players_to_buy:
            auth_token = AuthToken(headers_instance=self.headers_instance)
            auth_token.active_headers = self.active_headers

            captcha_solver = CaptchaSolver()
            captcha_solver.send_captcha_requests(players_to_buy)
            auth_token.get_auth_tokens(players_to_buy)
            self._get_item_buy_price(player_list=players_to_buy)

            players_to_buy_with_captcha_tokens = captcha_solver.get_captcha_tokens(
                players_to_buy
            )

            self._place_buy_orders(players_to_buy_with_captcha_tokens)
            print("DONE PLACING BUY ORDERS")

        return self.active_headers

    def _get_item_buy_price(self, player_list):
        """
        Updates each player in the list with the best current buy price.

        Args:
            player_list (list): Players to be updated with pricing info.
        """
        for player in player_list:
            player_uuid = player["URL"].split("/")[-1]
            response = requests.get(
                f"{self.single_item_api_path}?uuid={player_uuid}", timeout=10
            ).json()
            player["buy amount"] = response["best_buy_price"]

    def _place_buy_orders(self, player_list):
        """
        Places buy orders for the given list of players.

        Args:
            player_list (list): Players with all necessary tokens and prices.
        """
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
        """
        Injects the CAPTCHA token into the DOM for a given player's URL.

        Args:
            player_url (str): Webpage URL of the player.
            form_token (str): CAPTCHA token to inject.
        """
        self.driver.get(player_url)
        write_token_js = (
            f'document.getElementById("g-recaptcha-response").innerHTML="{form_token}";'
        )
        self.driver.execute_script(write_token_js)

    def _buy_order_post_request(
        self, player_url, buy_amount, form_token, auth_token_list
    ):
        """
        Submits a POST request to place a buy order using available auth tokens.

        Args:
            player_url (str): Endpoint URL for placing the order.
            buy_amount (float): Price to offer.
            form_token (str): CAPTCHA verification token.
            auth_token_list (list): List of authenticity tokens.

        Side Effects:
            Logs result of the order placement based on stubs balance comparison.
        """
        stubs_before = self.stubs.get_stubs_amount(url=player_url)

        for each in auth_token_list:
            form_data = {
                "authenticity_token": each,
                "price": buy_amount + BUY_ORDER_OVERBID,
                "g-recaptcha-response": form_token,
            }
            send_post = requests.post(
                f"{player_url}/create_buy_order",
                form_data,
                headers=self.active_headers,
                timeout=10,
            )

        stubs_after = self.stubs.get_stubs_amount(url=player_url)
        if stubs_before != stubs_after:
            print(send_post)
        else:
            print("ORDER NOT PLACED")
