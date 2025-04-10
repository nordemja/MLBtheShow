import time
import json
import undetected_chromedriver as uc

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserSession:
    def __init__(self, url, driver_version):
        self.url = url
        self.driver_version = driver_version
        self.browser = None
        self.session = None

    def start_browser(self):
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        self.browser = uc.Chrome(
            desired_capabilities=desired_capabilities, version_main=self.driver_version
        )
        self.browser.get(self.url)
        time.sleep(3)


# def get_new_browser_session(url, browser):
#     session_list = []

#     # Enable Performance Logging of Chrome.

#     browser.get(url)
#     time.sleep(3)
#     logs = browser.get_log("performance")

#     # Iterates every logs and parses it using JSON
#     for log in logs:
#         network_log = json.loads(log["message"])["message"]

#         # Checks if the current 'method' key has any
#         # Network related value.
#         if "Network.requestWillBeSentExtraInfo" in network_log["method"]:

#             try:
#                 x = network_log["params"]["headers"]["cookie"]
#                 new_session = x.split(";")

#                 for each in new_session:
#                     if ("_tsn_session=") in each:
#                         res = each.split("=")
#                         if res[1] not in session_list:
#                             session_list.append(res[1])

#             except:
#                 pass

#     print(session_list[-1])
#     return session_list[-1]
