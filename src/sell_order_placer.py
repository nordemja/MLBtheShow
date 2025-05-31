from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import requests
from bs4 import BeautifulSoup
from playsound import playsound

from config.globals import SELL_ORDER_OVERBID
from .captcha_solver import CaptchaSolver
from .auth_token import AuthToken


class SellOrderPlacer:
    """
    Responsible for executing sell orders on the MLB marketplace.

    This class handles the process of fetching item sell prices, solving CAPTCHA challenges,
    injecting CAPTCHA tokens into the webpage using Selenium, and submitting sell orders via HTTP requests.

    Attributes:
        single_item_api_path (str): API endpoint for retrieving item pricing details.
        headers (dict): HTTP headers used in all API and page requests.
        driver: Selenium WebDriver instance used for browser interaction.

    Methods:
        execute_sell_orders(players_to_sell: List[Dict[str, str]]) -> dict:
            Orchestrates the end-to-end process of placing sell orders.

        _get_item_sell_price(player_list: List[Dict[str, str]]):
            Retrieves the best sell price for each item via API.

        _get_total_sellable(player_url: str, headers: dict) -> int:
            Gets the total number of sellable items for a given player.

        _place_sell_orders(player_list: List[Dict[str, str]]):
            Performs the CAPTCHA injection and submits sell orders.

        _inject_captcha_token_into_webpage(player_url: str, form_token: str):
            Uses Selenium to inject the CAPTCHA token directly into the web page.

        _sell_order_post_request(player: Dict[str, any], sellable_before: int):
            Submits the actual sell order via HTTP POST request using player metadata.
    """

    def __init__(
        self,
        single_item_api_path: str,
        headers: dict,
        session,
        browser,
        error_sound_path,
    ):
        """
        Initializes the SellOrderPlacer instance.

        Args:
            single_item_api_path (str): The API endpoint to fetch single item data.
            headers (dict): The headers used in HTTP requests.
            browser: An object wrapping a Selenium WebDriver for page interaction.
        """
        self.single_item_api_path = single_item_api_path
        self.headers = headers
        self.session = session
        self.driver = browser.driver
        self.error_sound_path = error_sound_path
        self.active_headers = None

    def execute_sell_orders(self, players_to_sell: List[Dict[str, str]]):
        """
        Execute the process of selling orders, including CAPTCHA solving, authentication, and placing orders.

        Args:
            players_to_sell (List[Dict[str, str]]): List of players to sell.
        """
        print("Executing sell orders....")

        if players_to_sell:
            auth_token = AuthToken()

            captcha_solver = CaptchaSolver()
            captcha_solver.send_captcha_requests(players_to_sell)
            auth_token.get_auth_tokens(players_to_sell)
            self._get_item_sell_price(players_to_sell)

            sellable_players_with_captcha_tokens, leftover_player_list = (
                captcha_solver.get_captcha_tokens(players_to_sell)
            )
            self._place_sell_orders(sellable_players_with_captcha_tokens)

            if len(leftover_player_list) > 0:
                leftover_player_list_with_captcha_tokens, _ = (
                    captcha_solver.get_captcha_tokens(leftover_player_list)
                )
                self._place_sell_orders(leftover_player_list_with_captcha_tokens)

        print("DONE EXECUTING SELL ORDERS\n")

    def _get_item_sell_price(self, player_list: List[Dict[str, str]]):
        """
        Get the sell price for each player in the list.

        Args:
            player_list (List[Dict[str, str]]): The list of players to get sell prices for.
        """
        print("getting item sell prices.....")
        for player in player_list:
            player_uuid = player["URL"].split("/")[-1]
            response = requests.get(
                f"{self.single_item_api_path}?uuid={player_uuid}", timeout=10
            ).json()
            player["sell_price"] = response["best_sell_price"]

    def _get_total_sellable(self, player_url: str) -> int:
        """
        Get the total sellable count for a player.

        Args:
            playerURL (str): The URL of the player to check.
            headers (dict): The headers for HTTP requests.

        Returns:
            int: The number of sellable items for the player.
        """
        while True:
            try:
                player_page = self.session.get(
                    player_url, headers=self.headers, timeout=10
                )
                soup = BeautifulSoup(player_page.text, "html.parser")
                total_sellable = soup.find_all("div", {"class": "well"})
                for each in total_sellable:
                    if "Sellable" in each.text.strip():
                        total_sellable_cards = each.text.strip()[-1]
                        break
            except Exception as e:
                print(f"error: {e}")
                # self.headers_instance.get_and_update_new_auth_cookie(url=player_url)
                # self.active_headers = self.headers_instance.get_headers()
            else:
                return int(total_sellable_cards)

    def _place_sell_orders(self, player_list: List[Dict[str, str]]):
        """
        Place sell orders for each player in the list.

        Args:
            player_list (List[Dict[str, str]]): The list of players to place sell orders for.
        """
        for player in player_list:
            print(player["player name"])
            sellable_before = self._get_total_sellable(player_url=player["URL"])
            self._inject_captcha_token_into_webpage(
                player_url=player["URL"], form_token=player["form_token"]
            )
            self._sell_order_post_request(
                player=player,
                sellable_before=sellable_before,
            )

    def _inject_captcha_token_into_webpage(self, player_url: str, form_token: str):
        """
        Inject the CAPTCHA token into the webpage using Selenium.

        Args:
            player_url (str): The URL of the player to inject the CAPTCHA token into.
            form_token (str): The CAPTCHA form token to inject.
        """

        while True:
            try:
                print("loading page")
                self.driver.get(player_url)

                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.ID, "g-recaptcha-response"))
                )

                print("page loaded")

                write_token_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_token}";'

                self.driver.execute_script(write_token_js)

                print("injected captcha token")
                break

            except TimeoutException as e:
                playsound(self.error_sound_path)
                print(f"TimeoutException: {e}")
                self.driver.refresh()

            except WebDriverException as e:
                playsound(self.error_sound_path)
                print(f"WebDriverException: {e}")

            except Exception as e:
                print(f"Error: {e}")
                # self.headers_instance.get_and_update_new_auth_cookie()
                # self.active_headers = self.headers_instance.get_headers()

    def _sell_order_post_request(self, player: Dict[str, any], sellable_before: int):
        """
        Post a sell order for a player using their metadata.

        Args:
            player (Dict[str, any]): Dictionary containing player data including URL, form token, auth tokens,
                                     and price.
            sellable_before (int): Number of sellable items before placing the order.
        """
        for token in player["auth_token_list"]:
            form_data = {
                "authenticity_token": token,
                "price": player["sell_price"] - SELL_ORDER_OVERBID,
                "g-recaptcha-response": player["form_token"],
            }
            send_post = requests.post(
                player["URL"] + "/create_sell_order",
                form_data,
                headers=self.headers,
                timeout=10,
            )

        sellable_after = self._get_total_sellable(player_url=player["URL"])

        if sellable_after != sellable_before:
            print(sellable_after)
            print(send_post)
        else:
            print(sellable_after)
            print("ORDER NOT PLACED")
