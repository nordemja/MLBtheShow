from typing import List, Dict
import requests


class OrderChecker:
    """
    This class is responsible for checking buy and sell orders and taking actions
    based on the current market prices.

    It fetches the current best buy and sell prices for items using the provided API,
    compares those with the posted prices of buy and sell orders, and cancels orders if
    they have been undercut or outbid.

    Attributes:
        single_item_api_path (str): The API endpoint to fetch the current price of a single item.
        driver: Selenium WebDriver instance used to interact with the browser.
        player_list (List[Dict[str, str | int]]): A list that holds players whose orders were canceled.

    Methods:
        check_buy_orders(orders: List[Dict[str, str]]) -> List[Dict[str, str | int]]:
            Checks the buy orders to see if they are outbid and cancels them if so.

        check_sell_orders(orders: List[Dict[str, str]]) -> List[Dict[str, str | int]]:
            Checks the sell orders to see if they are undercut and cancels them if so.

        _cancel_order(order: Dict[str, str]):
            Cancels a specific order through Selenium browser interaction.

        _get_current_buy_amount(uuid: str) -> int:
            Retrieves the current best buy price for a player using the provided API.

        _get_current_sell_amount(uuid: str) -> int:
            Retrieves the current best sell price for a player using the provided API.
    """

    def __init__(self, single_item_api_path: str, browser):
        """
        Initialize OrderChecker.

        Args:
            single_item_api_path (str): The API endpoint for fetching a single item's data.
            browser: An object that wraps a Selenium WebDriver instance.
        """
        self.single_item_api_path = single_item_api_path
        self.driver = browser.driver

    def check_buy_orders(
        self, orders: List[Dict[str, str]]
    ) -> List[Dict[str, str | int]]:
        """
        Check each buy order to see if it's been outbid. Cancel and record if so.

        Args:
            orders (List[Dict[str, str]]): A list of buy orders.

        Returns:
            List[Dict[str, str | int]]: Players whose buy orders were canceled.
        """
        player_list: List[Dict[str, str | int]] = []
        for order in orders:
            uuid = order["URL"].split("/")[-1]
            current_buy_price = self._get_current_buy_amount(uuid)
            posted_price = int(order["Posted Price"])

            if posted_price < current_buy_price:
                player_list.append(
                    {
                        "player name": order["Name"],
                        "buy amount": current_buy_price,
                        "URL": order["URL"],
                    }
                )
                self._cancel_order(order)
            else:
                print(f"{order['Name']} at {posted_price} is currently best sell price")

        return player_list

    def check_sell_orders(
        self, orders: List[Dict[str, str]]
    ) -> List[Dict[str, str | int]]:
        """
        Check each sell order to see if it's been undercut. Cancel and record if so.

        Args:
            orders (List[Dict[str, str]]): A list of sell orders.

        Returns:
            List[Dict[str, str | int]]: Players whose sell orders were canceled.
        """
        player_list: List[Dict[str, str | int]] = []
        for order in orders:
            uuid = order["URL"].split("/")[-1]
            current_sell_price = self._get_current_sell_amount(uuid)
            posted_price = int(order["Posted Price"])

            if posted_price > current_sell_price:
                player_list.append(
                    {
                        "player name": order["Name"],
                        "sell amount": current_sell_price,
                        "URL": order["URL"],
                    }
                )
                self._cancel_order(order=order)
            else:
                print(f"{order['Name']} at {posted_price} is currently best buy price")

        return player_list

    def _cancel_order(self, order: Dict[str, str]):
        """
        Cancel a specific order using Selenium browser interaction.

        Args:
            order (Dict[str, str]): The order to cancel.
        """
        try:
            print(f"Cancelling order for {order['Name']}")
            self.driver.find_element(
                "xpath",
                f'//*[@id="{order["Order ID"]}"]/td[1]/form/button',
            ).click()
            self.driver.switch_to.alert.accept()

        except Exception as e:
            print(f"Failed to cancel order for {order['Name']}", e)

    def _get_current_buy_amount(self, uuid: str) -> int:
        """
        Get the current best buy price for a player.

        Args:
            uuid (str): The player's UUID.

        Returns:
            int: The current best buy price.
        """
        response = requests.get(
            f"{self.single_item_api_path}?uuid={uuid}", timeout=10
        ).json()
        current_buy_ammount = response["best_buy_price"]
        return int(current_buy_ammount)

    def _get_current_sell_amount(self, uuid: str) -> int:
        """
        Get the current best sell price for a player.

        Args:
            uuid (str): The player's UUID.

        Returns:
            int: The current best sell price.
        """
        response = requests.get(
            f"{self.single_item_api_path}?uuid={uuid}", timeout=10
        ).json()
        current_sell_ammount = response["best_sell_price"]
        return int(current_sell_ammount)
