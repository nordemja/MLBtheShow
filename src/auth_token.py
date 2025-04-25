import requests
from bs4 import BeautifulSoup


class AuthToken:
    """
    Handles the retrieval of authenticity tokens from player-specific URLs.

    This class is typically used to extract CSRF or session-specific tokens
    embedded in HTML forms on player detail pages.

    Attributes:
        headers (dict): The HTTP headers used for making GET requests to player-specific URLs.

    Methods:
        get_auth_tokens(player_list: list) -> None:
            Extracts authenticity tokens from each player's page and updates the player list with the tokens.

    """

    def __init__(self, headers_instance):
        """
        Initialize the AuthToken with required request headers.

        Args:
            headers (dict): HTTP headers to be used in GET requests.
        """
        self.headers_instance = headers_instance
        self.active_headers = self.headers_instance.get_headers()

    def get_auth_tokens(self, player_list):
        """
        Extract authenticity tokens from each player's page and update the player list.

        Args:
            player_list (list): A list of dictionaries where each dictionary must contain a "URL" key.
                                After processing, each dictionary will include an "auth_token_list" key
                                with a list of token values extracted from the page.

        """
        for player in player_list:
            while True:
                try:
                    auth_token_list = []
                    response = requests.get(
                        player["URL"], headers=self.active_headers, timeout=10
                    )
                    soup = BeautifulSoup(response.text, "html.parser")
                    form_tags = soup.find_all("input", {"name": "authenticity_token"})
                    for tag in form_tags:
                        auth_token_list.append(tag.get("value"))

                    player["auth_token_list"] = auth_token_list
                    break
                except Exception as e:
                    print(f"error: {e}")
                    self.headers_instance.get_and_update_new_auth_cookie(
                        url=player["URL"]
                    )
                    self.active_headers = self.headers_instance.get_headers()
