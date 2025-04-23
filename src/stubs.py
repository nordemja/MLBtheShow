from typing import Dict
from bs4 import BeautifulSoup
import requests


class Stubs:
    """
    Class to handle retrieving stubs balance from a given URL.

    Attributes:
        headers (Dict[str, str]): HTTP headers used for the request.

    Methods:
        get_stubs_amount(url: str) -> int:
            Retrieves the current stubs balance from the provided URL.
    """

    def __init__(self, headers: Dict[str, str]):
        """
        Initialize the Stubs class.

        Args:
            headers (Dict[str, str]): The headers to be used for HTTP requests.
        """
        self.headers = headers

    def get_stubs_amount(self, url: str) -> int:
        """
        Get the amount of stubs from the provided URL.

        Args:
            url (str): The URL from which to fetch the stubs amount.

        Returns:
            int: The amount of stubs as an integer.
        """
        stubs_amount = requests.get(url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(stubs_amount.text, "html.parser")
        stubs_amount = (
            soup.find("div", {"class": "well stubs"})
            .text.strip()
            .replace("Stubs Balance\n\n", "")
            .replace(",", "")
            .replace("Wallet\n", "")
        )
        return int(stubs_amount)
