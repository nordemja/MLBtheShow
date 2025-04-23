from typing import List, Dict
import os
import time
import requests

from config.globals import CAPTCHA_SOLVER_SEND_LINK, CAPTCHA_SOLVER_GET_TOKEN_LINK


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
        # try:
        for player in player_list:
            u1 = CAPTCHA_SOLVER_SEND_LINK.format(
                api_key=self.api_key,
                data_sitekey=self.data_sitekey,
                player_url=player["URL"],
            )
            response = requests.get(u1, timeout=10)
            request_id = int(response.json().get("request"))
            player["request_id"] = request_id
            # except Exception:
            #     print("FAILED SENDING TOKEN - TRYING AGAIN....")
            #     continue

    def get_captcha_tokens(self, player_list: List[Dict]) -> List[Dict]:
        """
        Retrieve CAPTCHA tokens from 2captcha API.

        Args:
            player_list (List[Dict]): List of player dictionaries with a "request_id" key.

        Returns:
            List[Dict]: List of player dictionaries with added "form_token" values.
        """
        ready_list = []
        start_time = time.time()
        i = 0
        while i < len(player_list):
            while True:
                try:
                    u2 = CAPTCHA_SOLVER_GET_TOKEN_LINK.format(
                        api_key=self.api_key, request_id=player_list[i]["request_id"]
                    )
                    response = requests.get(u2, timeout=10)
                    if response.json().get("status") == 1:
                        form_token = response.json().get("request")
                        player_list[i]["form_token"] = form_token
                        print(f"ACQUIRED TOKEN FOR {player_list[i]['player name']}")
                        ready_list.append(player_list[i])
                        i += 1
                    else:
                        # Move failed player to the end of the list and retry
                        player_list.append(
                            player_list.pop(player_list.index(player_list[i]))
                        )
                except Exception as e:
                    print(f"Error retrieving token: {e}")
                break

            elapsed_time = time.time() - start_time
            if elapsed_time > 60:
                break

        return ready_list
