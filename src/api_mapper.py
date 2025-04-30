from urllib.parse import urlparse, parse_qs, urlencode


class APIMapper:
    """
    Maps a web-based URL to a formatted API URL using a base API path and
    a dictionary mapping of team IDs.

    This class extracts query parameters from a given card series link and
    translates them into parameters compatible with the API format. It also
    applies custom transformations to specific parameters (e.g., renaming keys,
    mapping team IDs).

    Attributes:
        base_api_path (str): The base URL for the API endpoint.
        card_series_link (str): The original URL from the web interface to be parsed.
        team_id_map (dict): A dictionary that maps team IDs from the web interface to API-compatible values.
        params (dict): A dictionary of query parameters to be used in the final API URL.

    Methods:
        _parse_web_url() -> None:
            Parses the web URL to extract and map query parameters into the API-compatible format.

        get_api_url() -> str:
            Constructs and returns the full API URL including encoded query parameters.

        _map_team_id(value: str) -> None:
            Transforms team IDs from the web interface to the API-compatible format using the team ID map.

        _map_price_range(web_key: str, value: str) -> None:
            Transforms price range parameters (max and min buy price) into their API-compatible format.
    """

    def __init__(self, base_api_path, card_series_link, team_id_map):
        """
        Initialize the APIMapper with necessary configuration.

        Args:
            base_api_path (str): Base URL for the API endpoint.
            card_series_link (str): Original URL from the web interface to be parsed.
            team_id_map (dict): Dictionary mapping team IDs from the web interface to API-compatible values.
        """
        self.base_api_path = base_api_path
        self.card_series_link = card_series_link
        self.team_id_map = team_id_map
        self.params = {"page": 1}
        self._parse_web_url()

    def _parse_web_url(self):
        """
        Parse the card series web URL and convert query parameters to API-compatible format.

        This method:
        - Extracts query parameters from the URL.
        - Renames or maps certain keys for API compatibility.
        - Converts team IDs using the provided team_id_map.
        - Skips irrelevant parameters such as 'subdomain'.
        """
        parsed_url = urlparse(self.card_series_link)
        query_params = parse_qs(parsed_url.query)

        for web_key, values in query_params.items():
            web_key = web_key.split(";")[1]
            value = values[0] if values else None

            if web_key == "team_id":
                self._map_team_id(value)
            elif web_key in ["max_best_buy_price", "min_best_buy_price"]:
                self._map_price_range(web_key, value)
            elif web_key == "rarity_id":
                self._map_rarity(web_key, value)
            elif web_key == "subdomain":
                continue
            else:
                self.params[web_key] = value

    def _map_team_id(self, value: str):
        """
        Transforms team ID from the web interface into an API-compatible format.

        Args:
            value (str): The team ID value from the web URL to be mapped.
        """
        team_id = int(value)
        if team_id in self.team_id_map:
            self.params["team"] = self.team_id_map[team_id]

    def _map_rarity(self, web_key: str, value: str):

        web_key = "rarity"

        if value == "0":
            value = "common"
        elif value == "1":
            value = "bronze"
        elif value == "2":
            value = "silver"
        elif value == "3":
            value = "gold"
        else:
            value = "diamond"

        self.params[web_key] = value

    def _map_price_range(self, web_key: str, value: str):
        """
        Transforms price range parameters (max and min buy price) into API-compatible format.

        Args:
            web_key (str): The key for the price range parameter (either 'max_best_buy_price' or 'min_best_buy_price').
            value (str): The value associated with the price range parameter.
        """
        if web_key == "max_best_buy_price":
            web_key = "max_best_sell_price"

        # minimum buy now price
        elif web_key == "min_best_sell_price":
            web_key = "min_best_buy_price"

        # minimum sell now price
        elif web_key == "min_best_buy_price":
            web_key = "min_best_sell_price"

        self.params[web_key] = value

    def get_api_url(self) -> str:
        """
        Construct and return the full API URL with query parameters.

        Returns:
            str: The full API URL including encoded query parameters.
        """
        return f"{self.base_api_path}?{urlencode(self.params)}"
