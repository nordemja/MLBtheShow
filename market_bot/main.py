import requests
import traceback
import time
import json
import re
import undetected_chromedriver as uc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from playsound import playsound
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from tools import get_new_browser_session

error_sound_path = 'error_sound.mp3'
headers_path = 'headers.json'
base_path = "https://mlb23.theshow.com/"
data_sitekey = '6Leg5z4aAAAAABNstVp47FWPfKuOWeOtaGDayE6R'
API_KEY = "d912946a33a658ddf683e126d8551d07"

try:
    #header information to authenticate into account

    # def get_headers():
    #     filename = 'headers.json'
    #     with open(filename) as f:
    #         headers = json.load(f)
    #     return headers

    headers = get_headers()
    s = requests.Session()

    # def create_new_headers(session, headers):
    #     tempHeaders = headers['cookie'].split(';')
    #     new_cookie = ""
    #     for each in range(len(tempHeaders)):
    #         if "_tsn_session" in tempHeaders[each]:
    #             tempHeaders[each] = tempHeaders[each].split("=")[0] + "=" + session
            
    #         new_cookie += tempHeaders[each] + ";"

    #     new_cookie = new_cookie[:-1] + "" 
    #     headers['cookie'] = new_cookie

    #     newHeaders = json.dumps(headers)
    #     filename = 'headers.json'
    #     with open(filename, 'w') as outfile:
    #         outfile.write(newHeaders)

    # def getStubsAmount(data):
    #     stubsAmount = s.get(base_path + 'dashboard', headers= data)
    #     soup = BeautifulSoup(stubsAmount.text, 'html.parser')
    #     stubsAmount = soup.find('div', {'class': 'well stubs'}).text.strip().replace('Stubs Balance\n\n', '').replace(',','').replace('Wallet\n','')
    #     return int(stubsAmount)

    # def getBuyAmount(playerURL, data):
    #     amount_lst = []
    #     x = s.get(playerURL, headers= data)
    #     soup = BeautifulSoup(x.text, 'html.parser')
    #     buyAmountNew = soup.find_all('input', {'name': 'price'})
    #     for x in buyAmountNew:
    #         val = str(x).split(" ")[-1]
    #         prop = val.split("=")
    #         if prop[0] == "value":
    #             amount = int(re.findall(r'"([^"]*)"', prop[1])[0])
    #             amount_lst.append(amount)
    #     returnval = min(amount_lst)
    #     return returnval

    # def getSellAmount(playerURL, data):
    #     amount_lst = []
    #     x = s.get(playerURL, headers= data)
    #     soup = BeautifulSoup(x.text, 'html.parser')
    #     sellAmount = soup.find_all('input', {'name': 'price'})
    #     for x in sellAmount:
    #         val = str(x).split(" ")[-1]
    #         prop = val.split("=")
    #         if prop[0] == "value":
    #             amount = int(re.findall(r'"([^"]*)"', prop[1])[0])
    #             amount_lst.append(amount)
    #     returnval = max(amount_lst)
    #     return returnval

    # def getBuyAuthToken(playerURL, data):
    #     buyAuthList = []
    #     pageRequest = s.get(playerURL, headers= data)
    #     soup = BeautifulSoup(pageRequest.text, 'html.parser')
    #     buyForm = soup.find_all('input', {'name': 'authenticity_token'})
    #     for each in buyForm:
    #         buyAuthList.append(each.get('value'))
    #     return buyAuthList

    # def getSellAuthToken(playerURL, data):
    #     sellAuthList = []
    #     pageRequest = s.get(playerURL, headers= data)
    #     soup = BeautifulSoup(pageRequest.text, 'html.parser')
    #     sellForm = soup.find_all('input', {'name': 'authenticity_token'})
    #     for each in sellForm:
    #         sellAuthList.append(each.get('value'))
    #     return sellAuthList

    # # the below "Solver" function can be credited to 
    # # https://github.com/AiWorkshop/Selenium-Project/blob/master/part10-reCaptchaV2.py
    # def Solver(playerLst, driver, order, data, doubleCheck):
    #     authList = []
    #     failedOrderList = []
    #     readyList = []
    #     for each in playerLst:
    #         while True:
    #             try:
    #                 u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={each['URL']}&json=1&invisible=1"
    #                 r1 = s.get(u1)
    #                 requestID = int(r1.json().get('request'))
    #                 each['request_id'] = requestID
    #             except:
    #                 print("FAILED SENDING TOKEN - TRYING AGAIN....")
    #                 continue
    #             break
    #     startTime = time.time()
        
    #     #NEED HEADERS CHECK IN AUTH TOKEN AND AMOUNT FUNCTIONS
    #     for each in playerLst:
    #         if order == 'buy':
    #             attempts = 0
    #             while True:
    #                 try:
    #                     authTokenList = getBuyAuthToken(each['URL'], data)
    #                     each['auth token'] = authTokenList
    #                 except:
    #                     attempts += 1
    #                     if attempts == 5:
    #                         playsound(error_sound_path)
    #                         session = get_new_browser_session(cardSeriesLink, browser)
    #                         create_new_headers(session, data)
    #                         attempts = 0
    #                         data = get_headers()
    #                         continue
    #                 break
                
    #             attempts = 0
    #             while True:
    #                 try:
    #                     orderAmount = getBuyAmount(each['URL'], data)
    #                     each['buy amount'] = orderAmount
    #                 except:
    #                     attempts += 1
    #                     if attempts == 5:
    #                         playsound(error_sound_path)
    #                         session = get_new_browser_session(cardSeriesLink, browser)
    #                         create_new_headers(session, data)
    #                         attempts = 0
    #                         data = get_headers()
    #                         continue
    #                 break
    #         elif order == 'sell':
    #             attempts = 0
    #             while True:
    #                 try:
    #                     authToken = getSellAuthToken(each['URL'], data)
    #                     each['auth token'] = authToken
    #                 except:
    #                     attempts += 1
    #                     if attempts == 5:
    #                         playsound(error_sound_path)
    #                         session = get_new_browser_session(cardSeriesLink, browser)
    #                         create_new_headers(session, data)
    #                         attempts = 0
    #                         data = get_headers()
    #                         continue
    #                 break
                
    #             attempts = 0
    #             while True:
    #                 try:
    #                     orderAmount = getSellAmount(each['URL'], data)
    #                     each['sell amount'] = orderAmount
    #                 except:
    #                     attempts += 1
    #                     if attempts == 5:
    #                         playsound(error_sound_path)
    #                         session = get_new_browser_session(cardSeriesLink, browser)
    #                         create_new_headers(session, data)
    #                         attempts = 0
    #                         data = get_headers()
    #                         continue
    #                 break

    #     print('--------------------------------------------------------------------------------------------------------------------')
    #     i = 0
    #     while i < len(playerLst):

    #         while True:
    #             try:
    #                 u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={playerLst[i]['request_id']}&json=1"
    #                 r2 = s.get(u2)
    #                 if r2.json().get("status") == 1: 
    #                     form_tokon = r2.json().get("request")
    #                     playerLst[i]['form_token'] = form_tokon
    #                     print(f"ACQUIRED TOKEN FOR {playerLst[i]['player name']}")
    #                     readyList.append(playerLst[i])
    #                     i += 1
    #                 else:
    #                     playerLst.append(playerLst.pop(playerLst.index(playerLst[i])))
    #             except Exception as e:
    #                 print(e)
    #             break
            
    #         elapsed_time = time.time() - startTime
    #         if elapsed_time > 60:
    #             break

        
    #     for each in range(0,len(readyList)):
    #         if order == "buy":
    #             if doubleCheck:
    #                 print('placing new buy order for ' + readyList[each]['player name'])
    #             else:
    #                 print(readyList[each]['player name'])
                
    #             attempts = 0
    #             while True:
    #                 try:
    #                     driver.get(readyList[each]['URL'])
    #                     wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
    #                     driver.execute_script(wirte_tokon_js)
    #                     stubsBefore = getStubsAmount(data)
    #                     data = placeBuyOrder(readyList[each]['URL'], readyList[each]['buy amount'], readyList[each]['form_token'], readyList[each]['auth token'], stubsBefore, data)
    #                 except:
    #                     attempts += 1
    #                     if attempts == 5:
    #                         playsound(error_sound_path)
    #                         session = get_new_browser_session(cardSeriesLink, browser)
    #                         create_new_headers(session, data)
    #                         attempts = 0
    #                         data = get_headers()
    #                         continue
    #                 break

    #         if order == "sell":
    #             if doubleCheck:
    #                 print('placing new sell order for ' + playerLst[each]['player name'])
    #             else:
    #                 print(playerLst[each]['player name'])

    #             attempts = 0
    #             while True:
    #                 try:
    #                     driver.get(readyList[each]['URL'])
    #                     wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
    #                     driver.execute_script(wirte_tokon_js)
    #                     sellableBefore = getTotalSellable(readyList[each]['URL'], data)
    #                     data = placeSellOrder(readyList[each]['URL'], readyList[each]['sell amount'], readyList[each]['form_token'], readyList[each]['auth token'], sellableBefore, data)

    #                 except:
    #                     attempts += 1
    #                     if attempts == 5:
    #                         playsound(error_sound_path)
    #                         session = get_new_browser_session(cardSeriesLink, browser)
    #                         create_new_headers(session, data)
    #                         attempts = 0
    #                         data = get_headers()
    #                     continue
    #                 break

    #     if len(failedOrderList) > 0:
    #         Solver(failedOrderList, driver, 'sell', data, doubleCheck)

    #     return data


    def doRecaptcha(playerLst, webDriver, order, data, doubleCheck):

        if order == 'buy':
            data = Solver(playerLst, webDriver, order, data, doubleCheck)
        else:
            data = Solver(playerLst, webDriver, order, data, doubleCheck)
        
        return data
    
    def placeBuyOrder(playerURL, buyAmount, form_token, authToken, stubsBefore, data):

        for each in authToken:
            formData = {'authenticity_token': each, 'price': buyAmount, 'g-recaptcha-response': form_token}
            sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= data)
            stubsAfter = getStubsAmount(data)

            if stubsBefore != stubsAfter:
                print('i = ' + str(authToken.index(each)))
                print("length of authToken = " +str(len(authToken)))
                print(sendPost)
                break

        return data

    def placeSellOrder(playerURL, sellAmount, form_token, authTokenList, sellableBefore, data):
        for each in authTokenList:
            formData = {'authenticity_token': each, 'price': sellAmount - 5, 'g-recaptcha-response': form_token}
            sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= data)
            sellableAfter = getTotalSellable(playerURL,data)
            if sellableAfter != sellableBefore:
                 print(sellableAfter)
                 print('i = ' + str(authTokenList.index(each)))
                 print("length of authToken = " +str(len(authTokenList)))
                 print(sendPost)
                 break

        return data
    
    def getTotalSellable(playerURL, data):
        try:
            playerPage = s.get(playerURL, headers= data)
            soup = BeautifulSoup(playerPage.text, 'html.parser')
            totalSellable = soup.find_all('div', {'class': 'well'})[4].text.strip()[-1]
            return int(totalSellable)
        except Exception as e:
            print(e)


    def getOpenBuyOrdersList(data):
        buyOrders = []
        openOrdersPage = s.get(base_path + 'orders/buy_orders', headers= data)
        soup = BeautifulSoup(openOrdersPage.text, 'html.parser')

        try:
            ordersList = soup.find('tbody')
            openOrder = ordersList.find_all('tr')
            for each in openOrder:
                playerDict = {}
                playerName = each.contents[3].text.strip()
                postedPrice = each.contents[5].text.strip().replace(',','')
                orderID = each.get('id')
                playerURL = each.find('a')
                playerURL = 'https://mlb23.theshow.com' + playerURL['href'].lstrip().rstrip()
                playerDict['Name'] = playerName
                playerDict['Posted Price'] = postedPrice
                playerDict['URL'] = playerURL
                playerDict['Order ID'] = orderID
                buyOrders.append(playerDict)
            
            return buyOrders
        except AttributeError:
            return buyOrders


    def getOpenSellOrdersList(data):
        sellOrders = []
        try:
            openOrdersPage = s.get(base_path + 'orders/sell_orders', headers= data)
            soup = BeautifulSoup(openOrdersPage.text, 'html.parser')
            ordersList = soup.find('tbody')
            openOrder = ordersList.find_all('tr')
            for each in openOrder:
                playerDict = {}
                playerName = each.contents[3].text.strip()
                postedPrice = each.contents[5].text.strip().replace(',','')
                orderID = each.get('id')
                playerURL = each.find('a')
                playerURL = 'https://mlb23.theshow.com' + playerURL['href'].lstrip().rstrip()
                playerDict['Name'] = playerName
                playerDict['Posted Price'] = postedPrice
                playerDict['URL'] = playerURL
                playerDict['Order ID'] = orderID
                sellOrders.append(playerDict)

            return sellOrders

        except AttributeError:
            return sellOrders


    def getTotalOpenOrders(data):
        buyOrderList = getOpenBuyOrdersList(data)
        sellOrderList = getOpenSellOrdersList(data)
        return buyOrderList + sellOrderList
    
    #FINISH FIXING
    def doSellOrders(currentHeaders):

        print("Executing sell orders....")
        currentHeaders = get_headers()

        #get data from completed orders table
        attempts = 0
        while True:
            try:
                completedPage = s.get(base_path + 'orders/completed_orders', headers= currentHeaders)

                soup = BeautifulSoup(completedPage.text, 'html.parser')
                totalCompletedOrdersPages = soup.find('div', {'class': 'pagination'})
                totalCompletedOrdersPages = totalCompletedOrdersPages.find('a')
                testVar =  int(totalCompletedOrdersPages.text)
            except:
                attempts += 1
                if attempts == 5:
                    playsound(error_sound_path)
                    session = get_new_browser_session(cardSeriesLink, browser)
                    create_new_headers(session, currentHeaders)
                    currentHeaders = get_headers()
                    attempts = 0
                    continue
                continue
            break

        sellPlayerList = []
        for each in range(1, testVar+1):
            print("PAGE: " + str(each))
            cardsSellable = 1
            attempts = 0
            while True:
                try:
                    completedPage = s.get(base_path + 'orders/completed_orders?page='+str(each)+'&', headers= currentHeaders)
                    soup = BeautifulSoup(completedPage.text, 'html.parser')
                    playerOrderInfo = soup.find('tbody')
                    playerOrderInfo = playerOrderInfo.find_all('tr')
                except:
                    attempts += 1
                    if attempts == 5:
                        playsound(error_sound_path)
                        session = get_new_browser_session(cardSeriesLink, browser)
                        create_new_headers(session, currentHeaders)
                        currentHeaders = get_headers()
                        attempts = 0
                        continue
                    continue
                break
            
            for each in playerOrderInfo:
                cardsSellable = 1
                attempts = 0
                playerDict = {}
                while True:
                    try:
                    #loop through completed orders page and get time order was completed as datetime object

                        orderState = 0
                        requestName = each.contents[1].text.strip()
                        orderType = each.contents[3].text.strip().split()[0]
                        if orderType == 'Bought':
                            sellPlayerLink = each.find('a')
                            sellPlayerLink = 'https://mlb23.theshow.com' + sellPlayerLink['href'].lstrip().rstrip()
                            sellableBefore = getTotalSellable(sellPlayerLink, currentHeaders)
                            if sellableBefore > 0:
                                playerDict['player name'] = requestName
                                playerDict['URL'] = sellPlayerLink
                                sellPlayerList.append(playerDict)
                                print(requestName)
                                        
                            else:
                                cardsSellable = 0
                                
            
                    except:
                        attempts += 1
                        if attempts == 5:
                            if orderState == 1:
                                break
                            session = get_new_browser_session(cardSeriesLink, browser)
                            create_new_headers(session, currentHeaders)
                            currentHeaders = get_headers()
                            attempts = 0
                            continue
                        else:
                            if orderState == 1:
                                break
                            print("Failed " + str(attempts))
                            continue
                        
                    break

                if cardsSellable == 0:
                    break

            #Break out of page loop
            if cardsSellable == 0:
                break

        if len(sellPlayerList) > 0:
            print('\n')
            currentHeaders = doRecaptcha(sellPlayerList,browser,'sell',currentHeaders, False)

        print('DONE EXECUTING SELL ORDERS')
        return currentHeaders

    print(getStubsAmount(headers))

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    browser = uc.Chrome(desired_capabilities=desired_capabilities, version_main=112)

    browser.get(base_path + 'community_market')

    time.sleep(5)

    #specify which card series you want to search for

    cardSeriesLink = input('Enter Link of Card Criteria: ')
    # cardSeriesBase = base_path + 'community_market'
    # cardSeriesFilter = 'ma' + cardSeriesLink.strip(cardSeriesBase+'?page=')

    cardSeries = s.get(cardSeriesLink, headers = headers)

    browser.get(cardSeriesLink)



    #get total pages in card series

    soup = BeautifulSoup(cardSeries.text, 'html.parser')
    totalPagesFound = int(soup.find('h3').text.strip()[-1])
    print(totalPagesFound)


    headers = doSellOrders(headers)
    headers = get_headers()

    while True:
        try:
            #blank list of dicts to loop through to place buy order
            openListingLength = len(getTotalOpenOrders(headers))
            listings = []

            headers = get_headers()

            results = requests.get(base_path + 'apis/listings?max_best_buy_price=20000&min_best_buy_price=3000&series_id=1337').json()
            results = results['listings']

            for x in results:
                listingsDict = {}

                requestName = x['listing_name']
                buyAmount = int(x['best_buy_price']) + 5
                sellAmount = int(x['best_sell_price']) - 5
                profit = int((sellAmount) * .9) - buyAmount
                uuid = x['item']['uuid']
                link = base_path + f"items/{uuid}"

                listingsDict['player name'] = requestName
                listingsDict['buy amount'] = buyAmount
                listingsDict['sell amount'] = sellAmount
                listingsDict['profit'] = profit
                listingsDict['URL'] = link
                listings.append(listingsDict)

            #sort by highest profit
            listings = sorted(listings, key = lambda i: i['profit'])
            listings.reverse()  
            
            #place buy order for top 10 most profittable cards
            openOrderList = getTotalOpenOrders(headers)
            openListingLength = len(openOrderList)
            currentOpenBuyOrders = len(getOpenBuyOrdersList(headers))
            print('open buy orders = ' , currentOpenBuyOrders)

            playerList = []
            players = 0

            for each in listings:
                orderState = 0

                if any(d['Name'] == each['player name'] for d in openOrderList):
                    print(each['player name'])
                    pass
                else:
                    if currentOpenBuyOrders == 10 or openListingLength >= 25:
                        break
                    print(each)
                    playerList.append(each)
                    currentOpenBuyOrders += 1
                    openListingLength

            
            headers = doRecaptcha(playerList,browser,'buy',headers, False)

            headers = doSellOrders(headers)

            openBuyOrders = getOpenBuyOrdersList(headers)
            browser.get(base_path + 'orders/buy_orders')
            time.sleep(3)
            playerList = []
            for each in openBuyOrders:
                playerDict = {}
                attempts = 0
                while True:
                    try:
                        currentPrice = getBuyAmount(each['URL'], headers)
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
                
                if int(each['Posted Price']) < currentPrice:
                    playerDict['player name'] = each['Name']
                    playerDict['URL'] = each['URL']
                    while True:
                        try:
                            print("cancelling order for " + each['Name'])
                            browser.find_element("xpath", '//*[@id="'+each['Order ID']+'"]/td[1]/form/button').click()
                            browser.switch_to.alert.accept()
                            playerList.append(playerDict)
                            
                        except:

                            playsound(error_sound_path)
                            pass
                        break
                else:
                    print(each['Name'] + ' at ' + each['Posted Price'] + ' is currently best sell price')
            
            headers = doRecaptcha(playerList,browser,'buy',headers,True)
                            
            while True:
                try:
                    browser.get(base_path + 'orders/sell_orders')
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
                            currentSellAmount = getSellAmount(each['URL'],headers)
                        except:
                            attempts += 1
                            if attempts == 5:
                                playsound(error_sound_path)
                                session = get_new_browser_session(cardSeriesLink, browser)
                                create_new_headers(session, headers)
                                headers = get_headers()
                                attempts = 0
                            else:
                                print("Failed " + str(attempts))
                                continue
                        break
                    if int(each['Posted Price']) > currentSellAmount:
                        playerDict['player name'] = each['Name']
                        playerDict['URL'] = each['URL']
                        playerList.append(playerDict)
                        print("Cancelling " + each["Name"] + " at " + each["Posted Price"])
                        print(each["Posted Price"])
                        print(currentSellAmount)
                        try:
                            browser.find_element("xpath",'//*[@id="'+each["Order ID"]+'"]/td[1]/form/button').click()
                            browser.switch_to.alert.accept()
                        except:
                            pass

                    else:
                        print(each["Name"] + " at " + each["Posted Price"] + " is currently best buy price")
                except NoSuchElementException:
                    print("Order not found")

            headers = doRecaptcha(playerList,browser,'sell',headers,True)

                 
            headers = doSellOrders(headers)



        except KeyboardInterrupt:
            print("STOPPING PROGRAM")
            print('CANCELLING ORDERS...')
            break
except Exception:
    print(traceback.format_exc())
    playsound(error_sound_path)
