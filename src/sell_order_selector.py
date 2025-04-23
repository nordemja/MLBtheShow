from typing import List, Dict
import requests
from bs4 import BeautifulSoup


class SellOrderSelector:
    """
    Responsible for identifying players eligible for sell orders by analyzing completed
    transaction data and checking stock availability.

    Attributes:
        completed_orders_path (str): URL to fetch completed orders.
        headers (dict): HTTP headers used in all requests.

    Methods:
        fetch_sellable_players() -> List[Dict[str, str]]:
            Fetches completed orders and identifies players who are sellable based on the available stock.

        _get_orders_from_page(page: int) -> List:
            Fetches orders from a specific page on the completed orders list.

        _get_total_sellable(player_url: str, headers: dict) -> int:
            Gets the total number of sellable items for a given player.
    """

    def __init__(
        self,
        completed_orders_path: str,
        headers: dict,
    ):
        """
        Initializes the SellOrderSelector with the required request data.

        Args:
            completed_orders_path (str): The URL from which to fetch completed orders.
            headers (dict): HTTP headers to use in requests.
        """

        self.completed_orders_path = completed_orders_path
        self.headers = headers

    def fetch_sellable_players(self) -> List[Dict[str, str]]:
        """
        Fetch all completed orders and identify which players are sellable.

        Returns:
            List[Dict[str, str]]: A list of players who are sellable.
        """
        completed_page = requests.get(
            self.completed_orders_path, headers=self.headers, timeout=10
        )
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
                        break

            return sell_players

    def _get_orders_from_page(self, page: int) -> List:
        """
        Fetch orders for a specific page.

        Args:
            page (int): The page number to fetch orders from.

        Returns:
            List: The list of orders from the page.
        """
        resp = requests.get(
            f"{self.completed_orders_path}?page={page}&",
            headers=self.headers,
            timeout=10,
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.find("tbody").find_all("tr")

    def _get_total_sellable(self, player_url: str, headers: dict) -> int:
        """
        Get the total sellable count for a player.

        Args:
            playerURL (str): The URL of the player to check.
            headers (dict): The headers for HTTP requests.

        Returns:
            int: The number of sellable items for the player.
        """
        try:
            player_page = requests.get(player_url, headers=headers, timeout=10)
            soup = BeautifulSoup(player_page.text, "html.parser")
            total_sellable = soup.find_all("div", {"class": "well"})
            for each in total_sellable:
                if "Sellable" in each.text.strip():
                    total_sellable = each.text.strip()[-1]
                    return int(total_sellable)
        except Exception as e:
            print(e)

        return 0
