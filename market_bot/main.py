import requests
import traceback
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from playsound import playsound
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from tools import get_new_browser_session
from amounts import getStubsAmount, getBuyAmount, getSellAmount
from headers import get_headers, create_new_headers
from open_orders import getTotalOpenOrders, getOpenBuyOrdersList, getOpenSellOrdersList
from get_total_sellable import getTotalSellable
from solver import doRecaptcha, doSellOrders
from globals import base_path, error_sound_path
from webdriver_manager.chrome import ChromeDriverManager


try:

    init_headers = get_headers()

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    # browser = ChromeDriverManager().install()
    browser = uc.Chrome(desired_capabilities=desired_capabilities, version_main=114)

    browser.get(base_path + "community_market")

    # specify which card series you want to search for
    cardSeriesLink = input("Enter Link of Card Criteria: ")
    session = get_new_browser_session(cardSeriesLink, browser)
    create_new_headers(session, init_headers)

    headers = get_headers()

    print(getStubsAmount(headers))

    cardSeriesFilter = cardSeriesLink.strip(base_path + "/community_market?page=")
    cardSeries = requests.get(cardSeriesLink, headers=headers)

    browser.get(cardSeriesLink)

    # get total pages in card series

    soup = BeautifulSoup(cardSeries.text, "html.parser")
    totalPagesFound = int(soup.find("h3").text.strip()[-1])
    print(totalPagesFound)

    headers = doSellOrders(headers, cardSeriesLink, browser)
    headers = get_headers()

    while True:
        try:
            # blank list of dicts to loop through to place buy order
            openListingLength = len(getTotalOpenOrders(headers))
            listings = []

            headers = get_headers()

            for each in range(1, totalPagesFound + 1):
                while True:
                    try:

                        print(
                            base_path
                            + "/community_market?page="
                            + str(each)
                            + "&"
                            + cardSeriesFilter
                        )
                        searchReults = requests.get(
                            base_path
                            + "/community_market?page="
                            + str(each)
                            + "&"
                            + cardSeriesFilter,
                            headers=headers,
                        )
                        soup = BeautifulSoup(searchReults.text, "html.parser")
                        table = soup.find("tbody")
                        results = table.find_all("tr")

                        for x in results:
                            listingsDict = {}

                            for y in x.contents:
                                print(y.text.strip())

                            print(
                                "----------------------------------------------------------------------------------"
                            )

                            # requestName =  x.contents[5].text.strip()
                            # buyAmount = x.contents[11].text.strip()
                            # sellAmount = x.contents[9].text.strip()
                            # profit = int((sellAmount) * .9) - buyAmount
                            # uuid = x.find('a')
                            # link = base_path + uuid['href'].lstrip().rstrip().strip('fave')

                            # listingsDict['player name'] = requestName
                            # listingsDict['buy amount'] = buyAmount
                            # listingsDict['sell amount'] = sellAmount
                            # listingsDict['profit'] = profit
                            # listingsDict['URL'] = link
                            # listingsDict['sellable'] = getTotalSellable(link, headers)
                            # listings.append(listingsDict)

                    except:
                        print("break")
                    break

            # results = requests.get(base_path + 'apis/listings?max_best_buy_price=35000&set_name=SET 2').json()
            # results = results['listings']

            # for x in results:
            #     listingsDict = {}

            #     requestName = x['listing_name']
            #     buyAmount = int(x['best_buy_price']) + 25
            #     sellAmount = int(x['best_sell_price']) - 25
            #     profit = int((sellAmount) * .9) - buyAmount
            #     uuid = x['item']['uuid']
            #     link = base_path + f"items/{uuid}"

            # listingsDict['player name'] = requestName
            # listingsDict['buy amount'] = buyAmount
            # listingsDict['sell amount'] = sellAmount
            # listingsDict['profit'] = profit
            # listingsDict['URL'] = link
            # listingsDict['sellable'] = getTotalSellable(link, headers)
            # listings.append(listingsDict)

            # sort by highest profit
            listings = sorted(listings, key=lambda i: i["profit"])
            listings.reverse()

            # place buy order for top 10 most profittable cards
            openOrderList = getTotalOpenOrders(headers)
            openListingLength = len(openOrderList)
            currentOpenBuyOrders = len(getOpenBuyOrdersList(headers))
            print("open buy orders = ", currentOpenBuyOrders)

            playerList = []
            players = 0

            for each in listings:
                orderState = 0

                if any(d["Name"] == each["player name"] for d in openOrderList):
                    print(each["player name"])
                    pass
                if each["sellable"] > 0:
                    print(each["player name"])
                    print("CARD ALREADY OWNED AND READY TO BE SOLD")
                    pass
                else:
                    if currentOpenBuyOrders == 10 or openListingLength >= 25:
                        break
                    print(each)
                    playerList.append(each)
                    currentOpenBuyOrders += 1
                    openListingLength

            headers = doRecaptcha(
                playerList, browser, "buy", headers, False, cardSeriesLink, browser
            )

            headers = doSellOrders(headers, cardSeriesLink, browser)

            openBuyOrders = getOpenBuyOrdersList(headers)
            browser.get(base_path + "orders/buy_orders")
            time.sleep(3)
            playerList = []
            for each in openBuyOrders:
                playerDict = {}
                attempts = 0
                while True:
                    try:
                        currentPrice = getBuyAmount(each["URL"], headers)
                    except:
                        attempts += 1
                        if attempts == 5:
                            playsound(error_sound_path)
                            session = get_new_browser_session(cardSeriesLink, browser)
                            create_new_headers(session, headers)
                            headers = get_headers()
                            attempts = 0
                            continue
                        else:
                            print("Failed once")
                            continue
                    break

                if int(each["Posted Price"]) < currentPrice:
                    playerDict["player name"] = each["Name"]
                    playerDict["URL"] = each["URL"]
                    while True:
                        try:
                            print("cancelling order for " + each["Name"])
                            browser.find_element(
                                "xpath",
                                '//*[@id="' + each["Order ID"] + '"]/td[1]/form/button',
                            ).click()
                            browser.switch_to.alert.accept()
                            playerList.append(playerDict)

                        except:

                            playsound(error_sound_path)
                            pass
                        break
                else:
                    print(
                        each["Name"]
                        + " at "
                        + each["Posted Price"]
                        + " is currently best sell price"
                    )

            headers = doRecaptcha(
                playerList, browser, "buy", headers, True, cardSeriesLink, browser
            )

            while True:
                try:
                    browser.get(base_path + "orders/sell_orders")
                except:
                    continue
                break
            time.sleep(3)
            openSellOrders = getOpenSellOrdersList(headers)

            playerList = []
            for each in openSellOrders:
                playerDict = {}
                orderState = 0
                attempts = 0
                try:
                    while True:
                        try:
                            currentSellAmount = getSellAmount(each["URL"], headers)
                        except:
                            attempts += 1
                            if attempts == 5:
                                playsound(error_sound_path)
                                session = get_new_browser_session(
                                    cardSeriesLink, browser
                                )
                                create_new_headers(session, headers)
                                headers = get_headers()
                                attempts = 0
                            else:
                                print("Failed " + str(attempts))
                                continue
                        break
                    if int(each["Posted Price"]) > currentSellAmount:
                        playerDict["player name"] = each["Name"]
                        playerDict["URL"] = each["URL"]
                        playerList.append(playerDict)
                        print(
                            "Cancelling " + each["Name"] + " at " + each["Posted Price"]
                        )
                        print(each["Posted Price"])
                        print(currentSellAmount)
                        try:
                            browser.find_element(
                                "xpath",
                                '//*[@id="' + each["Order ID"] + '"]/td[1]/form/button',
                            ).click()
                            browser.switch_to.alert.accept()
                        except:
                            pass

                    else:
                        print(
                            each["Name"]
                            + " at "
                            + each["Posted Price"]
                            + " is currently best buy price"
                        )
                except NoSuchElementException:
                    print("Order not found")

            headers = doRecaptcha(
                playerList, browser, "sell", headers, True, cardSeriesLink, browser
            )

            headers = doSellOrders(headers, cardSeriesLink, browser)

        except KeyboardInterrupt:
            print("STOPPING PROGRAM")
            print("CANCELLING ORDERS...")
            break
except Exception:
    print(traceback.format_exc())
    playsound(error_sound_path)
