import requests


class Market:
    """
    A class to interact with the market API, fetch listings, and process them for buying and selling.

    This class is responsible for:
    - Fetching market listings by querying multiple pages of the API.
    - Extracting relevant data from the listings, such as player name, buy amount, sell amount, and profit.
    - Sorting the listings by profit in descending order.

    Attributes:
        root_path (str): The root URL for the market items.
        api_url (str): The API endpoint URL for fetching market listings.
        api_mapper (ApiMapper): An instance of ApiMapper to handle URL parameters.
        listings (list): A list of processed listings, containing player name, buy amount, sell amount, profit, and URL.
    """

    def __init__(self, root_path: str, api_url: str, api_mapper):
        """
        Initialize the Market class to interact with the API and fetch market listings.

        Args:
            root_path (str): The root URL for the market items.
            api_url (str): The API endpoint URL for fetching the market listings.
            api_mapper: An instance of ApiMapper to handle URL parameters.
        """
        self.root_path = root_path
        self.api_url = api_url
        self.api_mapper = api_mapper
        self.listings = []

    def fetch_listings(self) -> list:
        """
        Fetch market listings by retrieving all pages and processing the data.

        Iterates through all available pages, updates the API request URL, and processes each market page to
        extract the listings.

        Returns:
            list: A list of listings sorted by profit, each containing details like player name, buy amount,
                  sell amount, profit, and URL.
        """
        total_pages = self._fetch_total_pages()
        for page in range(1, total_pages + 1):
            self.api_mapper.params["page"] = page
            updated_page_url = self.api_mapper.get_api_url()
            self._process_market_page(updated_page_url)

        return self._sort_by_profit(self.listings)

    def _fetch_total_pages(self) -> int:
        """
        Fetch the total number of pages from the API response.

        Sends a GET request to the API and parses the JSON response to retrieve the total pages.

        Returns:
            int: The total number of pages available for the market listings.
        """
        listings_json = requests.get(self.api_url, timeout=10).json()
        return listings_json["total_pages"]

    def _process_market_page(self, api_link: str) -> None:
        """
        Process a single market page and extract listing data.

        Sends a GET request to the provided API link, parses the response, and then iterates over the listings
        to extract player data.

        Args:
            api_link (str): The API URL for the specific page of listings to fetch.
        """
        results_metadata = requests.get(api_link, timeout=10).json()
        master_listings = results_metadata["listings"]

        for listing in master_listings:
            player_data = self._extract_listing_data(listing)
            if player_data:
                self.listings.append(player_data)

    def _extract_listing_data(self, player: dict) -> dict:
        """
        Extract relevant data from a single player listing.

        Parses the listing data to extract the player's name, buy amount, sell amount, and calculates profit.

        Args:
            player (dict): The player listing data from the API.

        Returns:
            dict: A dictionary containing the player's name, buy amount, sell amount, profit, and URL.
                  Returns None if there was an error extracting the data.
        """
        try:
            request_name = player["listing_name"]
            buy_amount = int(player["best_buy_price"])
            sell_amount = int(player["best_sell_price"])
            profit = int(sell_amount * 0.9) - buy_amount
            uuid = player["item"]["uuid"]
            url = f"{self.root_path}/items/{uuid}"

            return {
                "player name": request_name,
                "buy amount": buy_amount,
                "sell amount": sell_amount,
                "profit": profit,
                "URL": url,
            }
        except Exception as e:
            print(f"Error extracting listing: {e}")
            return None

    def _sort_by_profit(self, listings: list) -> list:
        """
        Sort listings by profit in descending order.

        Sorts the list of listings based on the calculated profit, with the highest profit first.

        Args:
            listings (list): The list of player listings to sort.

        Returns:
            list: The sorted list of listings, sorted by profit in descending order.
        """
        return sorted(listings, key=lambda x: x["profit"], reverse=True)
