import traceback
import os
import time
from playsound import playsound

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.common.exceptions import NoSuchElementException
# from tools import get_new_browser_session
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
from src.order_checker import OrderChecker

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
            players_to_sell = sell_orders.fetch_sellable_players()
            headers = sell_orders.execute_sell_orders()

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

            players_to_buy = buy_orders.select_players()

            headers = buy_orders.execute_buy_orders(players_to_buy=players_to_buy)

            players_to_sell = sell_orders.fetch_sellable_players()
            headers = sell_orders.execute_sell_orders(players_to_sell=players_to_sell)

            open_buy_orders = open_buy_orders.get_buy_orders()
            browser.get(base_path + "orders/buy_orders")
            time.sleep(3)

            order_checker = OrderChecker(
                single_item_api_path=SINGLE_ITEM_LISTING_API_PATH
            )

            replace_buy_orders = order_checker.check_buy_orders(open_buy_orders)

            headers = buy_orders.execute_buy_orders(replace_buy_orders)

            browser.get(base_path + "orders/sell_orders")
            time.sleep(3)
            open_sell_orders = getOpenSellOrdersList(headers)

            replace_sell_orders = order_checker.check_sell_orders()

            sell_orders.execute_sell_orders(replace_sell_orders)

        except KeyboardInterrupt:
            print("STOPPING PROGRAM")
            print("CANCELLING ORDERS...")
            headers.delete_cookie()
            exit()
except Exception:
    headers.delete_cookie()
    print(traceback.format_exc())
    playsound(error_sound_path)
