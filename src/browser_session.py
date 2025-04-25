import time
import json
import sys
import undetected_chromedriver as uc

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserSession:
    """
    Handles launching a stealth browser session and extracting authentication cookies.

    This class uses undetected_chromedriver (uc) to bypass bot detection and
    Selenium to interact with Chrome, retrieve browser logs, and parse cookies
    relevant for authenticated web driver access and GET requests.

    Attributes:
        session_cookie (str): The authentication cookies extracted from the browser session.
        driver (uc.Chrome): The instance of the Chrome web driver used for session interaction.
        allowed_keys (set): Set of cookie keys to be extracted from the browser logs.

    Methods:
        start_browser() -> None:
            Launches a Chrome browser session with a specific user profile
            and enables logging of performance (network) events.

        close_browser() -> None:
            Closes the currently running browser session.

        get_cookie_header_from_browser(url: str) -> None:
            Navigates to a specified URL and retrieves authentication cookies
            from the browser's performance logs.

        _parse_cookie(cookie_str: str) -> str:
            Filters and formats cookies from a raw cookie string, keeping only allowed keys.
    """

    def __init__(self):
        """
        Initialize the BrowserSession with a predefined set of allowed cookie keys.
        """
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
        """
        Launch a Chrome browser session with a specific user profile and
        enable logging of performance (network) events.
        """
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        options = uc.ChromeOptions()
        options.add_argument("--user-data-dir=C:/Users/justi/chrome_user_data_copy")
        options.add_argument("--profile-directory=Default")

        self.driver = uc.Chrome(
            options=options, desired_capabilities=desired_capabilities
        )

    def close_browser(self):
        """
        Close the currently running browser session.
        """
        self.driver.quit()

    def get_cookie_header_from_browser(self, url):
        """
        Navigate to a specified URL and retrieve authentication cookies
        from Chrome's performance logs. Stores the parsed cookies internally.

        Args:
            url (str): The URL to visit in the browser.

        Side effects:
            Sets self.session_cookie with the extracted cookie header.
        """
        print("getting auth cookie......")
        self.driver.get(url)
        time.sleep(10)

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
        sys.exit()

    def _parse_cookie(self, cookie_str):
        """
        Filters and formats cookies from a raw cookie string.

        Args:
            cookie_str (str): Raw cookie string from browser logs.

        Returns:
            str: A filtered and concatenated cookie string containing only allowed keys.
        """
        cookies = ""
        for item in cookie_str.split("; "):
            if "=" in item:
                key, value = item.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key in self.allowed_keys:
                    cookies += key + "=" + value + "; "

        return cookies.rstrip("; ").strip()
