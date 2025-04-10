import traceback
import os

# import time
# import undetected_chromedriver as uc
# from bs4 import BeautifulSoup
from playsound import playsound

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.common.exceptions import NoSuchElementException
# from tools import get_new_browser_session
# from amounts import getStubsAmount, getBuyAmount, getSellAmount
# from headers import get_headers, create_new_headers
# from open_orders import getTotalOpenOrders, getOpenBuyOrdersList, getOpenSellOrdersList
# from get_total_sellable import getTotalSellable
# from solver import doRecaptcha, doSellOrders
from config.globals import BASE_PATH, HEADERS_PATH, ERROR_SOUND_PATH

# from webdriver_manager.chrome import ChromeDriverManager

from src.headers import get_headers

from src.browser_session import BrowserSession
from src.stubs import Stubs
from src.market import Market


try:

    error_sound_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config", ERROR_SOUND_PATH
    )
    headers_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config", HEADERS_PATH
    )

    card_series_link = input("Enter Link of Card Criteria: ")

    headers = get_headers(headers_file_path)
    browser_session = BrowserSession(BASE_PATH)
    browser_session.start_browser()

    stubs = Stubs(BASE_PATH, headers)
    market = Market(card_series_link, headers, browser_session.browser)

    print(f"Stubs Balance: {stubs.get_stubs_amount()}")
    total_pages_found = market.fetch_total_pages()
    print(total_pages_found)

    # session = get_new_browser_session(card_series_link, browser)
    # create_new_headers(session, init_headers)

    # browser.get(card_series_link)

    # headers = doSellOrders(headers, card_series_link, browser)
    # headers = get_headers()

    # while True:
    #     try:
    #         # blank list of dicts to loop through to place buy order
    #         open_listing_length = len(getTotalOpenOrders(headers))
    #         listings = []

    #         headers = get_headers()

    #         for each in range(1, total_pages_found + 1):
    #             while True:
    #                 try:

    #                     print(
    #                         base_path
    #                         + "/community_market?page="
    #                         + str(each)
    #                         + "&"
    #                         + card_series_filter
    #                     )
    #                     search_reults = requests.get(
    #                         base_path
    #                         + "/community_market?page="
    #                         + str(each)
    #                         + "&"
    #                         + card_series_filter,
    #                         headers=headers,
    #                     )
    #                     soup = BeautifulSoup(search_reults.text, "html.parser")
    #                     table = soup.find("tbody")
    #                     results = table.find_all("tr")

    #                     for x in results:
    #                         listings_dict = {}

    #                         for y in x.contents:
    #                             print(y.text.strip())

    #                         print(
    #                             "----------------------------------------------------------------------------------"
    #                         )

    #                         # requestName =  x.contents[5].text.strip()
    #                         # buyAmount = x.contents[11].text.strip()
    #                         # sellAmount = x.contents[9].text.strip()
    #                         # profit = int((sellAmount) * .9) - buyAmount
    #                         # uuid = x.find('a')
    #                         # link = base_path + uuid['href'].lstrip().rstrip().strip('fave')

    #                         # listings_dict['player name'] = requestName
    #                         # listings_dict['buy amount'] = buyAmount
    #                         # listings_dict['sell amount'] = sellAmount
    #                         # listings_dict['profit'] = profit
    #                         # listings_dict['URL'] = link
    #                         # listings_dict['sellable'] = getTotalSellable(link, headers)
    #                         # listings.append(listings_dict)

    #                 except:
    #                     print("break")
    #                 break

    #         # results = requests.get(base_path + 'apis/listings?max_best_buy_price=35000&set_name=SET 2').json()
    #         # results = results['listings']

    #         # for x in results:
    #         #     listings_dict = {}

    #         #     requestName = x['listing_name']
    #         #     buyAmount = int(x['best_buy_price']) + 25
    #         #     sellAmount = int(x['best_sell_price']) - 25
    #         #     profit = int((sellAmount) * .9) - buyAmount
    #         #     uuid = x['item']['uuid']
    #         #     link = base_path + f"items/{uuid}"

    #         # listings_dict['player name'] = requestName
    #         # listings_dict['buy amount'] = buyAmount
    #         # listings_dict['sell amount'] = sellAmount
    #         # listings_dict['profit'] = profit
    #         # listings_dict['URL'] = link
    #         # listings_dict['sellable'] = getTotalSellable(link, headers)
    #         # listings.append(listings_dict)

    #         # sort by highest profit
    #         listings = sorted(listings, key=lambda i: i["profit"])
    #         listings.reverse()

    #         # place buy order for top 10 most profittable cards
    #         open_order_list = getTotalOpenOrders(headers)
    #         open_listing_length = len(open_order_list)
    #         current_open_buy_orders = len(getOpenBuyOrdersList(headers))
    #         print("open buy orders = ", current_open_buy_orders)

    #         player_list = []
    #         players = 0

    #         for each in listings:
    #             order_state = 0

    #             if any(d["Name"] == each["player name"] for d in open_order_list):
    #                 print(each["player name"])
    #                 pass
    #             if each["sellable"] > 0:
    #                 print(each["player name"])
    #                 print("CARD ALREADY OWNED AND READY TO BE SOLD")
    #                 pass
    #             else:
    #                 if current_open_buy_orders == 10 or open_listing_length >= 25:
    #                     break
    #                 print(each)
    #                 player_list.append(each)
    #                 current_open_buy_orders += 1
    #                 open_listing_length

    #         headers = doRecaptcha(
    #             player_list, browser, "buy", headers, False, card_series_link, browser
    #         )

    #         headers = doSellOrders(headers, card_series_link, browser)

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

    #         headers = doSellOrders(headers, card_series_link, browser)

    #     except KeyboardInterrupt:
    #         print("STOPPING PROGRAM")
    #         print("CANCELLING ORDERS...")
    #         break
except Exception:
    print(traceback.format_exc())
    playsound(error_sound_path)
