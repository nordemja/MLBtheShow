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

    def __init__(self):
        """
        Initialize the AuthToken with required request headers.

        Args:
            headers (dict): HTTP headers to be used in GET requests.
        """

    def get_auth_tokens(self, html):
        """
        Extract authenticity tokens from a block of HTML.

        Args:
            html (str): HTML content as a string.

        Returns:
            list: A list of authenticity token values extracted from the HTML.
        """

        print("Extracting auth tokens from HTML...")
        auth_token_list = []
        soup = BeautifulSoup(html, "html.parser")

        # Extract from meta tags (only if csrf-param is authenticity_token)
        csrf_param = soup.find(
            "meta", {"name": "csrf-param", "content": "authenticity_token"}
        )
        if csrf_param:
            csrf_token_tag = soup.find("meta", {"name": "csrf-token"})
            if csrf_token_tag and csrf_token_tag.get("content"):
                auth_token_list.append(csrf_token_tag["content"])

        # Extract from input tags
        input_tags = soup.find_all("input", {"name": "authenticity_token"})
        for tag in input_tags:
            value = tag.get("value")
            if value:
                auth_token_list.append(value)

        return auth_token_list
