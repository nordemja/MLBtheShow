import traceback
import os
import time
from playsound import playsound

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.common.exceptions import NoSuchElementException
# from tools import get_new_browser_session
# from headers import get_headers, create_new_headers
# from open_orders import getTotalOpenOrders, getOpenBuyOrdersList, getOpenSellOrdersList
from config.globals import (
    ROOT_PATH,
    BASE_API_PATH,
    SINGLE_ITEM_LISTING_API_PATH,
    COMMUNITY_MARKET_PATH,
    OPEN_ORDERS_PATH,
    COMPLETED_ORDERS_PATH,
    HEADERS_PATH,
    ERROR_SOUND_PATH,
)

from config.team_id_map import TEAM_ID_MAP

# from webdriver_manager.chrome import ChromeDriverManager

from src.headers import Headers

from src.browser_session import BrowserSession
from src.stubs import Stubs
from src.api_mapper import APIMapper
from src.market import Market
from src.buy_orders import BuyOrders
from src.sell_orders import SellOrders
from src.open_orders import OpenOrders

# session = get_new_browser_session(card_series_link, browser)
# create_new_headers(session, init_headers)

try:

    error_sound_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config", ERROR_SOUND_PATH
    )
    headers_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config", HEADERS_PATH
    )

    browser = BrowserSession(community_market_path=COMMUNITY_MARKET_PATH)
    browser.start_browser()
    browser.get_cookie_header_from_browser(url=COMMUNITY_MARKET_PATH)

    auth_cookie = browser.session_cookie

    headers = Headers(headers_file_path)
    headers.update_cookie(auth_cookie)

    active_headers = headers.get_headers()
    print(active_headers)

    stubs = Stubs(active_headers)
    print(f"Stubs Balance: {stubs.get_stubs_amount(COMMUNITY_MARKET_PATH)}")

    exit()

    card_series_link = input("Enter Link of Card Criteria: ")
    # browser.set_page(card_series_link)

    sell_orders = SellOrders(
        SINGLE_ITEM_LISTING_API_PATH, COMPLETED_ORDERS_PATH, headers, browser
    )
    open_orders = OpenOrders(OPEN_ORDERS_PATH, headers)

    api_mapper = APIMapper(BASE_API_PATH, card_series_link, TEAM_ID_MAP)
    api_url = api_mapper.get_api_url()
    market = Market(ROOT_PATH, api_url, api_mapper)

    while True:
        try:
            # headers = sell_orders.execute_sell_orders()

            listings = market.fetch_listings()

            # place buy order for top 10 most profittable cards
            open_order_list = open_orders.get_all_open_orders()
            current_buy_order_length = len(open_orders.get_buy_orders())
            open_listing_length = len(open_order_list)
            print("open buy orders = ", current_buy_order_length)

            buy_orders = BuyOrders(
                COMMUNITY_MARKET_PATH,
                listings,
                open_order_list,
                current_buy_order_length,
                open_listing_length,
                headers,
                browser,
            )
            headers = buy_orders.execute_buy_orders()

            headers = sell_orders.execute_sell_orders()

        #         open_buy_orders = getOpenBuyOrdersList(headers)
        #         browser.get(base_path + "orders/buy_orders")
        #         time.sleep(3)
        #         player_list = []
        #         for each in open_buy_orders:
        #             player_dict = {}
        #             attempts = 0
        #             while True:
        #                 try:
        #                     current_price = getBuyAmount(each["URL"], headers)
        #                 except:
        #                     attempts += 1
        #                     if attempts == 5:
        #                         playsound(error_sound_path)
        #                         session = get_new_browser_session(card_series_link, browser)
        #                         create_new_headers(session, headers)
        #                         headers = get_headers()
        #                         attempts = 0
        #                         continue
        #                     else:
        #                         print("Failed once")
        #                         continue
        #                 break

        #             if int(each["Posted Price"]) < current_price:
        #                 player_dict["player name"] = each["Name"]
        #                 player_dict["URL"] = each["URL"]
        #                 while True:
        #                     try:
        #                         print("cancelling order for " + each["Name"])
        #                         browser.find_element(
        #                             "xpath",
        #                             '//*[@id="' + each["Order ID"] + '"]/td[1]/form/button',
        #                         ).click()
        #                         browser.switch_to.alert.accept()
        #                         player_list.append(player_dict)

        #                     except:

        #                         playsound(error_sound_path)
        #                         pass
        #                     break
        #             else:
        #                 print(
        #                     each["Name"]
        #                     + " at "
        #                     + each["Posted Price"]
        #                     + " is currently best sell price"
        #                 )

        #         headers = doRecaptcha(
        #             player_list, browser, "buy", headers, True, card_series_link, browser
        #         )

        #         while True:
        #             try:
        #                 browser.get(base_path + "orders/sell_orders")
        #             except:
        #                 continue
        #             break
        #         time.sleep(3)
        #         open_sell_orders = getOpenSellOrdersList(headers)

        #         player_list = []
        #         for each in open_sell_orders:
        #             player_dict = {}
        #             order_state = 0
        #             attempts = 0
        #             try:
        #                 while True:
        #                     try:
        #                         current_sell_amount = getSellAmount(each["URL"], headers)
        #                     except:
        #                         attempts += 1
        #                         if attempts == 5:
        #                             playsound(error_sound_path)
        #                             session = get_new_browser_session(
        #                                 card_series_link, browser
        #                             )
        #                             create_new_headers(session, headers)
        #                             headers = get_headers()
        #                             attempts = 0
        #                         else:
        #                             print("Failed " + str(attempts))
        #                             continue
        #                     break
        #                 if int(each["Posted Price"]) > current_sell_amount:
        #                     player_dict["player name"] = each["Name"]
        #                     player_dict["URL"] = each["URL"]
        #                     player_list.append(player_dict)
        #                     print(
        #                         "Cancelling " + each["Name"] + " at " + each["Posted Price"]
        #                     )
        #                     print(each["Posted Price"])
        #                     print(current_sell_amount)
        #                     try:
        #                         browser.find_element(
        #                             "xpath",
        #                             '//*[@id="' + each["Order ID"] + '"]/td[1]/form/button',
        #                         ).click()
        #                         browser.switch_to.alert.accept()
        #                     except:
        #                         pass

        #                 else:
        #                     print(
        #                         each["Name"]
        #                         + " at "
        #                         + each["Posted Price"]
        #                         + " is currently best buy price"
        #                     )
        #             except NoSuchElementException:
        #                 print("Order not found")

        #         headers = doRecaptcha(
        #             player_list, browser, "sell", headers, True, card_series_link, browser
        #         )

        except KeyboardInterrupt:
            print("STOPPING PROGRAM")
            print("CANCELLING ORDERS...")
            break
except Exception:
    print(traceback.format_exc())
    playsound(error_sound_path)
