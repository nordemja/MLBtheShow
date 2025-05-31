# import time
# import json
# import sys
import requests
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
        self.driver = None

    def start_browser(self):
        """
        Launch a Chrome browser session with a specific user profile and
        enable logging of performance (network) events.
        """

        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        )

        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument(f"--user-agent={user_agent}")
        options.add_argument("--user-data-dir=C:/Users/justi/jnordeman")
        options.add_argument("--profile-directory=Profile 2")

        self.driver = uc.Chrome(
            options=options, desired_capabilities=desired_capabilities
        )

    def close_browser(self):
        """
        Close the currently running browser session.
        """
        self.driver.quit()

    def create_requests_session(self, driver) -> requests.Session:
        """
        Create a requests.Session object using cookies from a Selenium WebDriver.

        Args:
            driver (WebDriver): The Selenium WebDriver instance containing cookies
                                from an authenticated browser session.

        Returns:
            requests.Session: A session preloaded with the browser's cookies for use in HTTP requests.

        Side effects:
            Uses cookies from the provided WebDriver instance to populate the session object.
        """
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])
        return session
