from typing import List, Dict
import os
import time
import requests


class CaptchaSolver:
    """
    A class to interact with the 2Captcha API to solve CAPTCHA challenges.

    This class is responsible for sending CAPTCHA solving requests to 2Captcha's API and retrieving
    the solved CAPTCHA tokens, which can then be used for further processing.

    Attributes:
        api_key (str): API key to authenticate with the 2Captcha service.
        data_sitekey (str): The site key required for CAPTCHA solving, specific to the service being used.

    Methods:
        send_captcha_requests(player_list: List[Dict]): Sends CAPTCHA solving requests for a list of players.
        get_captcha_tokens(player_list: List[Dict]): Retrieves the solved CAPTCHA tokens for a list of players.
    """

    def __init__(self):
        """
        Initialize the CaptchaSolver with the API endpoints and environment variables.
        """
        self.api_key = os.getenv("two_captcha_api_key")
        self.data_sitekey = os.getenv("mlb_the_show_data_sitekey")

    def send_captcha_requests(self, player_list: List[Dict]) -> None:
        """
        Send requests to 2captcha API to solve CAPTCHA.

        Args:
            player_list (List[Dict]): List of player dictionaries with a "URL" key.
        """
        for player in player_list:
            url = (
                f"https://2captcha.com/in.php?key={self.api_key}"
                f"&method=userrecaptcha"
                f"&googlekey={self.data_sitekey}"
                f"&pageurl={player['URL']}"
                f"&json=1&invisible=1"
            )
            response = requests.get(url, timeout=10)
            request_id = int(response.json().get("request"))
            player["request_id"] = request_id

    def get_captcha_tokens(self, player_list: List[Dict]) -> List[Dict]:
        """
        Retrieves the solved CAPTCHA tokens for a list of players from the 2Captcha API.

        This method checks the status of CAPTCHA solving requests and waits for the tokens to be ready.
        If a token is not ready, the player is moved to the end of the list and the process retries.
        The process continues until all players have their CAPTCHA tokens.

        Args:
            player_list (List[Dict]): List of player dictionaries, each containing a "request_id" key
                                    representing a CAPTCHA request that has been sent to the 2Captcha API.

        Returns:
            List[Dict]: List of player dictionaries with the additional key containing the solved CAPTCHA token.
        """
        ready_list = []
        start_time = time.time()
        i = 0
        while i < len(player_list):
            while True:
                try:
                    request_id = player_list[i]["request_id"]
                    url = (
                        f"https://2captcha.com/res.php?key={self.api_key}"
                        f"&action=get&id={request_id}&json=1"
                    )
                    response = requests.get(url, timeout=10)
                    if response.json().get("status") == 1:
                        form_token = response.json().get("request")
                        player_list[i]["form_token"] = form_token
                        print(f"ACQUIRED TOKEN FOR {player_list[i]['player name']}")
                        ready_list.append(player_list[i])
                        i += 1
                    else:
                        player_list.append(player_list.pop(i))
                except Exception as e:
                    print(f"Error retrieving token: {e}")
                break

            if time.time() - start_time > 60:
                break

        return ready_list
