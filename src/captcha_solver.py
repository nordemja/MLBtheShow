import os
import time
import requests


class CaptchaSolver:
    def __init__(self):
        self.api_key = os.getenv("two_captcha_api_key")
        self.data_sitekey = os.getenv("mlb_the_show_data_sitekey")

    def send_captcha_requests(self, player_list):
        """Send requests to 2captcha API to solve CAPTCHA."""
        # try:
        for player in player_list:
            u1 = f"https://2captcha.com/in.php?key={self.api_key}&method=userrecaptcha&googlekey={self.data_sitekey}&pageurl={player['URL']}&json=1&invisible=1"
            response = requests.get(u1)
            request_id = int(response.json().get("request"))
            player["request_id"] = request_id
            # except Exception:
            #     print("FAILED SENDING TOKEN - TRYING AGAIN....")
            #     continue

    def get_captcha_tokens(self, player_list):
        """Retrieve CAPTCHA tokens from 2captcha API."""
        ready_list = []
        start_time = time.time()
        i = 0
        while i < len(player_list):
            while True:
                try:
                    u2 = f"https://2captcha.com/res.php?key={self.api_key}&action=get&id={player_list[i]['request_id']}&json=1"
                    response = requests.get(u2)
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
