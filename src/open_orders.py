from typing import List, Dict
from bs4 import BeautifulSoup
import requests


class OpenOrders:
    """
    Retrieves and parses open buy and sell orders from web pages.

    This class fetches the HTML content of specified pages for open buy and sell orders,
    parses the order details using BeautifulSoup, and returns the extracted information.

    Attributes:
        open_buy_orders_path (str): URL for the page containing open buy orders.
        open_sell_orders_path (str): URL for the page containing open sell orders.
        headers (dict): HTTP headers to be included in the requests.

    Methods:
        get_buy_orders() -> List[Dict[str, str]]:
            Retrieves a list of open buy orders.

        get_sell_orders() -> List[Dict[str, str]]:
            Retrieves a list of open sell orders.

        get_all_open_orders() -> List[Dict[str, str]]:
            Retrieves a combined list of all open orders (both buy and sell).

        _get_orders(order_type: str) -> List[Dict[str, str]]:
            Helper method to retrieve orders of a specific type ("buy" or "sell").
    """

    def __init__(
        self, open_buy_orders_path: str, open_sell_orders_path: str, headers: dict
    ):
        """
        Initialize OpenOrders with URLs and headers.

        Args:
            open_buy_orders_path (str): URL to the open buy orders page.
            open_sell_orders_path (str): URL to the open sell orders page.
            headers (dict): Headers for the HTTP request.
        """
        self.open_buy_orders_path = open_buy_orders_path
        self.open_sell_orders_path = open_sell_orders_path
        self.headers = headers

    def get_buy_orders(self) -> List[Dict[str, str]]:
        """
        Retrieve a list of open buy orders.

        Returns:
            List[Dict[str, str]]: A list of buy order dictionaries.
        """
        return self._get_orders("buy")

    def get_sell_orders(self) -> List[Dict[str, str]]:
        """
        Retrieve a list of open sell orders.

        Returns:
            List[Dict[str, str]]: A list of sell order dictionaries.
        """
        return self._get_orders("sell")

    def get_all_open_orders(self) -> List[Dict[str, str]]:
        """
        Retrieve all open orders (both buy and sell).

        Returns:
            List[Dict[str, str]]: Combined list of all open orders.
        """
        return self.get_buy_orders() + self.get_sell_orders()

    def _get_orders(self, order_type: str) -> List[Dict[str, str]]:
        """
        Helper method to retrieve orders of a specific type.

        Args:
            order_type (str): Type of order to retrieve ("buy" or "sell").

        Returns:
            List[Dict[str, str]]: A list of order dictionaries.
        """
        order_list: List[Dict[str, str]] = []
        if order_type == "buy":
            url = self.open_buy_orders_path
        else:
            url = self.open_sell_orders_path

        response = requests.get(url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            rows = soup.find("tbody").find_all("tr")
            for row in rows:
                player_name = row.contents[3].text.strip()
                posted_price = row.contents[5].text.strip().replace(",", "")
                order_id = row.get("id")
                player_url = "https://mlb23.theshow.com" + row.find("a")["href"].strip()

                order_list.append(
                    {
                        "Name": player_name,
                        "Posted Price": posted_price,
                        "URL": player_url,
                        "Order ID": order_id,
                    }
                )
        except AttributeError:
            pass

        return order_list
