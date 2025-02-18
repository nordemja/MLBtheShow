import requests
import time
from globals import API_KEY, data_sitekey, error_sound_path, base_path
from auth_token import getBuyAuthToken, getSellAuthToken
from tools import get_new_browser_session
from headers import create_new_headers, get_headers
from amounts import getBuyAmount, getSellAmount, getStubsAmount
from get_total_sellable import getTotalSellable
from place_orders import placeBuyOrder, placeSellOrder
from playsound import playsound
from bs4 import BeautifulSoup


def do_sell_orders(current_headers, cardSeriesLink, browser):

    print("Executing sell orders....")
    current_headers = get_headers()

    # get data from completed orders table
    attempts = 0
    while True:
        try:
            completed_page = requests.get(
                base_path + "orders/completed_orders", headers=current_headers
            )

            soup = BeautifulSoup(completed_page.text, "html.parser")
            total_completed_orders_pages = soup.find("div", {"class": "pagination"})
            total_completed_orders_pages = total_completed_orders_pages.find("a")
            test_var = int(total_completed_orders_pages.text)
        except:
            attempts += 1
            if attempts == 5:
                playsound(error_sound_path)
                session = get_new_browser_session(cardSeriesLink, browser)
                create_new_headers(session, current_headers)
                current_headers = get_headers()
                attempts = 0
                continue
            continue
        break

    sell_player_list = []
    for each in range(1, test_var + 1):
        print("PAGE: " + str(each))
        cards_sellable = 1
        attempts = 0
        while True:
            try:
                completed_page = requests.get(
                    base_path + "orders/completed_orders?page=" + str(each) + "&",
                    headers=current_headers,
                )
                soup = BeautifulSoup(completed_page.text, "html.parser")
                player_order_info = soup.find("tbody")
                player_order_info = player_order_info.find_all("tr")
            except:
                attempts += 1
                if attempts == 5:
                    playsound(error_sound_path)
                    session = get_new_browser_session(cardSeriesLink, browser)
                    create_new_headers(session, current_headers)
                    current_headers = get_headers()
                    attempts = 0
                    continue
                continue
            break

        for each in player_order_info:
            cards_sellable = 1
            attempts = 0
            player_dict = {}
            while True:
                try:
                    # loop through completed orders page and get time order was completed as datetime object

                    order_state = 0
                    request_name = each.contents[1].text.strip()
                    order_type = each.contents[3].text.strip().split()[0]
                    if order_type == "Bought":
                        sell_player_link = each.find("a")
                        sell_player_link = (
                            "https://mlb23.theshow.com"
                            + sell_player_link["href"].lstrip().rstrip()
                        )
                        sellable_before = getTotalSellable(
                            sell_player_link, current_headers
                        )
                        if sellable_before > 0:
                            player_dict["player name"] = request_name
                            player_dict["URL"] = sell_player_link
                            sell_player_list.append(player_dict)
                            print(request_name)

                        else:
                            cards_sellable = 0

                except:
                    attempts += 1
                    if attempts == 5:
                        if order_state == 1:
                            break
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, current_headers)
                        current_headers = get_headers()
                        attempts = 0
                        continue
                    else:
                        if order_state == 1:
                            break
                        print("Failed " + str(attempts))
                        continue

                break

            if cards_sellable == 0:
                break

        # Break out of page loop
        if cards_sellable == 0:
            break

    if len(sell_player_list) > 0:
        print("\n")
        current_headers = do_recaptcha(
            sell_player_list,
            browser,
            "sell",
            current_headers,
            False,
            cardSeriesLink,
            browser,
        )

    print("DONE EXECUTING SELL ORDERS")
    return current_headers


def do_recaptcha(
    playerLst, webDriver, order, data, doubleCheck, cardSeriesLink, browser
):

    if order == "buy":
        data = solver(
            playerLst, webDriver, order, data, doubleCheck, cardSeriesLink, browser
        )
    else:
        data = solver(
            playerLst, webDriver, order, data, doubleCheck, cardSeriesLink, browser
        )

    return data


# the below "solver" function can be credited to
# https://github.com/AiWorkshop/Selenium-Project/blob/master/part10-reCaptchaV2.py
def solver(playerLst, driver, order, data, doubleCheck, cardSeriesLink, browser):
    auth_list = []
    failed_order_list = []
    ready_list = []
    for each in playerLst:
        while True:
            try:
                u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={each['URL']}&json=1&invisible=1"
                r1 = requests.get(u1)
                request_i_d = int(r1.json().get("request"))
                each["request_id"] = request_i_d
            except:
                print("FAILED SENDING TOKEN - TRYING AGAIN....")
                continue
            break
    start_time = time.time()

    # NEED HEADERS CHECK IN AUTH TOKEN AND AMOUNT FUNCTIONS
    for each in playerLst:
        if order == "buy":
            attempts = 0
            while True:
                try:
                    auth_token_list = getBuyAuthToken(each["URL"], data)
                    each["auth token"] = auth_token_list
                except:
                    attempts += 1
                    if attempts == 5:
                        playsound(error_sound_path)
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, data)
                        attempts = 0
                        data = get_headers()
                        continue
                break

            attempts = 0
            while True:
                try:
                    order_amount = getBuyAmount(each["URL"], data)
                    each["buy amount"] = order_amount
                except:
                    attempts += 1
                    if attempts == 5:
                        playsound(error_sound_path)
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, data)
                        attempts = 0
                        data = get_headers()
                        continue
                break
        elif order == "sell":
            attempts = 0
            while True:
                try:
                    auth_token = getSellAuthToken(each["URL"], data)
                    each["auth token"] = auth_token
                except:
                    attempts += 1
                    if attempts == 5:
                        playsound(error_sound_path)
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, data)
                        attempts = 0
                        data = get_headers()
                        continue
                break

            attempts = 0
            while True:
                try:
                    order_amount = getSellAmount(each["URL"], data)
                    each["sell amount"] = order_amount
                except:
                    attempts += 1
                    if attempts == 5:
                        playsound(error_sound_path)
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, data)
                        attempts = 0
                        data = get_headers()
                        continue
                break

    print(
        "--------------------------------------------------------------------------------------------------------------------"
    )
    i = 0
    while i < len(playerLst):

        while True:
            try:
                u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={playerLst[i]['request_id']}&json=1"
                r2 = requests.get(u2)
                if r2.json().get("status") == 1:
                    form_tokon = r2.json().get("request")
                    playerLst[i]["form_token"] = form_tokon
                    print(f"ACQUIRED TOKEN FOR {playerLst[i]['player name']}")
                    ready_list.append(playerLst[i])
                    i += 1
                else:
                    playerLst.append(playerLst.pop(playerLst.index(playerLst[i])))
            except Exception as e:
                print(e)
            break

        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            break

    for each in range(0, len(ready_list)):
        if order == "buy":
            if doubleCheck:
                print("placing new buy order for " + ready_list[each]["player name"])
            else:
                print(ready_list[each]["player name"])

            attempts = 0
            while True:
                try:
                    driver.get(ready_list[each]["URL"])
                    wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
                    driver.execute_script(wirte_tokon_js)
                    stubs_before = getStubsAmount(data)
                    data = placeBuyOrder(
                        ready_list[each]["URL"],
                        ready_list[each]["buy amount"],
                        ready_list[each]["form_token"],
                        ready_list[each]["auth token"],
                        stubs_before,
                        data,
                    )
                except:
                    attempts += 1
                    if attempts == 5:
                        playsound(error_sound_path)
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, data)
                        attempts = 0
                        data = get_headers()
                        continue
                break

        if order == "sell":
            if doubleCheck:
                print("placing new sell order for " + playerLst[each]["player name"])
            else:
                print(playerLst[each]["player name"])

            attempts = 0
            while True:
                try:
                    driver.get(ready_list[each]["URL"])
                    wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
                    driver.execute_script(wirte_tokon_js)
                    sellable_before = getTotalSellable(ready_list[each]["URL"], data)
                    data = placeSellOrder(
                        ready_list[each]["URL"],
                        ready_list[each]["sell amount"],
                        ready_list[each]["form_token"],
                        ready_list[each]["auth token"],
                        sellable_before,
                        data,
                    )

                except:
                    attempts += 1
                    if attempts == 5:
                        playsound(error_sound_path)
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, data)
                        attempts = 0
                        data = get_headers()
                    continue
                break

    if len(failed_order_list) > 0:
        solver(failed_order_list, driver, "sell", data, doubleCheck)

    return data
