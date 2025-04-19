import time
import json
from urllib.parse import urlparse
import undetected_chromedriver as uc

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserSession:
    def __init__(self, community_market_path):
        self.community_market_path = community_market_path
        self.session_cookie = None
        self.driver = None
        self.allowed_keys = {
            "tsn_token",
            "ab.storage.userId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5",
            "ab.storage.deviceId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5",
            "tsn_item_referrer",
            "_gid",
            "_tsn_session",
            "ab.storage.sessionId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5",
            "_ga",
            "tsn_last_url",
            "_ga_EJKYYHZPBF",
        }

    def start_browser(self):
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        options = uc.ChromeOptions()
        options.add_argument("--user-data-dir=C:/Users/justi/chrome_user_data_copy")
        options.add_argument("--profile-directory=Profile 2")

        self.driver = uc.Chrome(
            options=options, desired_capabilities=desired_capabilities
        )

    def get_cookie_header_from_browser(self, url):
        self.driver.get(url)
        time.sleep(10)
        self.driver.get(url)  # Let it fully load and send requests

        logs = self.driver.get_log("performance")
        for entry in logs:
            try:
                log = json.loads(entry["message"])["message"]
                if (
                    log["method"] == "Network.requestWillBeSentExtraInfo"
                    and "headers" in log["params"]
                    and "cookie" in log["params"]["headers"]
                ):
                    full_browser_cookie = log["params"]["headers"]["cookie"]
                    self.session_cookie = self._parse_cookie(full_browser_cookie)
                    return  # Grab the first valid one and break
            except Exception:
                continue

        print("ERROR: No cookie header found.")
        exit()

    def _parse_cookie(self, cookie_str):
        cookies = ""
        for item in cookie_str.split("; "):
            if "=" in item:
                key, value = item.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key in self.allowed_keys:
                    cookies += key + "=" + value + "; "

        return cookies.rstrip("; ").strip()
