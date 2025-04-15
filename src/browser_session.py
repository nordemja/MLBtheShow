import time
import json
from urllib.parse import urlparse
import undetected_chromedriver as uc

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserSession:
    def __init__(self, headers):
        self.headers = headers
        self.driver = None

    def start_browser(self, url):
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = uc.Chrome(
            options=options, desired_capabilities=desired_capabilities
        )

        self.driver.get(url)
        time.sleep(3)
        self._login(url)

    def _login(self, url):
        self.driver.delete_all_cookies()
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        cookie_header = self.headers.get("cookie", "")
        for cookie_pair in cookie_header.split("; "):
            if "=" in cookie_pair:
                name, value = cookie_pair.split("=", 1)
                cookie = {
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": domain,
                    "path": "/",
                }
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Couldn't add cookie {name}: {e}")

        self.driver.get(url)

    def get_new_browser_session(url, browser):
        session_list = []

        # Enable Performance Logging of Chrome.

        browser.get(url)
        time.sleep(3)
        logs = browser.get_log("performance")

        # Iterates every logs and parses it using JSON
        for log in logs:
            network_log = json.loads(log["message"])["message"]

            # Checks if the current 'method' key has any
            # Network related value.
            if "Network.requestWillBeSentExtraInfo" in network_log["method"]:

                try:
                    x = network_log["params"]["headers"]["cookie"]
                    new_session = x.split(";")

                    for each in new_session:
                        if ("_tsn_session=") in each:
                            res = each.split("=")
                            if res[1] not in session_list:
                                session_list.append(res[1])

                except:
                    pass

        print(session_list[-1])
        return session_list[-1]
