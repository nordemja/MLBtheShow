import traceback
import os
import time
from playsound import playsound
from config.globals import (
    ROOT_PATH,
    BASE_API_PATH,
    SINGLE_ITEM_LISTING_API_PATH,
    OPEN_BUY_ORDERS_PATH,
    OPEN_SELL_ORDERS_PATH,
    COMPLETED_ORDERS_PATH,
    GET_REQUEST_HEADERS_PATH,
    POST_REQUEST_HEADERS_PATH,
    ERROR_SOUND_PATH,
)
from config.team_id_map import TEAM_ID_MAP

from src.headers import Headers
from src.browser_session import BrowserSession
from src.stubs import Stubs
from src.api_mapper import APIMapper
from src.market import Market
from src.buy_order_selector import BuyOrderSelector
from src.buy_order_placer import BuyOrderPlacer
from src.sell_order_selector import SellOrderSelector
from src.sell_order_placer import SellOrderPlacer
from src.open_orders import OpenOrders
from src.order_checker import OrderChecker

# get path to config files
error_sound_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "config", ERROR_SOUND_PATH
)
get_request_headers_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "config", GET_REQUEST_HEADERS_PATH
)

post_request_headers_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "config", POST_REQUEST_HEADERS_PATH
)

try:

    # start browser that will be used for automation
    browser = BrowserSession()
    browser.start_browser()

    # get cards that will be used for flipping
    card_series_link = input(
        "Log into the communinty market and enter link of card criteria: "
    )

    session = browser.create_requests_session(browser.driver)

    # dynamically set user authentication cookie
    # browser.get_cookie_header_from_browser(url=card_series_link)
    headers_instance = Headers(error_sound_path=error_sound_path)
    headers_get_request = headers_instance.get_headers(get_request_headers_file_path)
    headers_post_request = headers_instance.get_headers(post_request_headers_file_path)
    # headers_instance.update_cookie(new_cookie=browser.session_cookie)

    # get available stubs balance
    stubs = Stubs(headers=headers_get_request, requests_session=session)
    print(f"Stubs Balance: {stubs.get_stubs_amount(url=card_series_link)}\n")

    # intalize rest of classes to be used
    buy_order_selector = BuyOrderSelector(
        listings=None,
        open_orders=None,
        buy_order_length=None,
        total_open_listing_length=None,
    )

    buy_order_placer = BuyOrderPlacer(
        single_item_api_path=SINGLE_ITEM_LISTING_API_PATH,
        headers=headers_post_request,
        session=session,
        browser=browser,
        error_sound_path=error_sound_path,
    )

    sell_order_selector = SellOrderSelector(
        completed_orders_path=COMPLETED_ORDERS_PATH,
        root_path=ROOT_PATH,
        headers=headers_get_request,
        session=session,
    )

    sell_order_placer = SellOrderPlacer(
        single_item_api_path=SINGLE_ITEM_LISTING_API_PATH,
        headers=headers_post_request,
        session=session,
        browser=browser,
        error_sound_path=error_sound_path,
    )

    open_orders = OpenOrders(
        open_buy_orders_path=OPEN_BUY_ORDERS_PATH,
        open_sell_orders_path=OPEN_SELL_ORDERS_PATH,
        root_path=ROOT_PATH,
        headers=headers_get_request,
        session=session,
    )

    api_mapper = APIMapper(
        base_api_path=BASE_API_PATH,
        card_series_link=card_series_link,
        team_id_map=TEAM_ID_MAP,
    )

    API_URL = api_mapper.get_api_url()

    market = Market(root_path=ROOT_PATH, api_url=API_URL, api_mapper=api_mapper)

    while True:
        try:
            # get players to sell as a list then place sell orders
            players_to_sell = sell_order_selector.fetch_sellable_players()

            sell_order_placer.execute_sell_orders(players_to_sell=players_to_sell)

            # fetch all players available to flip from API and order by profit margin
            listings = market.fetch_listings()

            open_order_list = open_orders.get_all_open_orders()
            CURRENT_BUY_ORDER_LENGTH = len(open_orders.get_buy_orders())
            OPEN_LISTING_LENGTH = len(open_order_list)
            print("open buy orders = ", CURRENT_BUY_ORDER_LENGTH, "\n")

            buy_order_selector.listings = listings
            buy_order_selector.open_orders = open_order_list
            buy_order_selector.buy_order_length = CURRENT_BUY_ORDER_LENGTH
            buy_order_selector.total_open_listing_length = OPEN_LISTING_LENGTH

            # get players to buy as a list
            players_to_buy = buy_order_selector.select_players()
            print("\n")

            # place buy orders
            buy_order_placer.execute_buy_orders(players_to_buy=players_to_buy)

            # get players to buy as a list then place buy orders
            players_to_sell = sell_order_selector.fetch_sellable_players()
            sell_order_placer.execute_sell_orders(players_to_sell=players_to_sell)

            # get a list of the currently open buy orders
            open_buy_orders = open_orders.get_buy_orders()
            browser.driver.get(OPEN_BUY_ORDERS_PATH)
            time.sleep(3)

            order_checker = OrderChecker(
                single_item_api_path=SINGLE_ITEM_LISTING_API_PATH, browser=browser
            )

            # check that active buy order is best price, cancel and replace order if not
            replace_buy_orders = order_checker.check_buy_orders(orders=open_buy_orders)

            buy_order_placer.execute_buy_orders(players_to_buy=replace_buy_orders)

            # get a list of the currently open sell orders
            open_sell_orders = open_orders.get_sell_orders()
            browser.driver.get(OPEN_SELL_ORDERS_PATH)
            time.sleep(3)

            # check that active buy order is best price, cancel and replace order if not
            replace_sell_orders = order_checker.check_sell_orders(
                orders=open_sell_orders
            )

            sell_order_placer.execute_sell_orders(players_to_sell=replace_sell_orders)

        except KeyboardInterrupt:
            print("STOPPING PROGRAM")
            print("CANCELLING ORDERS...")
            browser.close_browser()
except Exception as e:
    browser.close_browser()
    print(e)
    print(traceback.format_exc())
    playsound(error_sound_path)
