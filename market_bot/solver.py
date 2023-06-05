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


def doSellOrders(currentHeaders, cardSeriesLink, browser):

    print("Executing sell orders....")
    currentHeaders = get_headers()

    #get data from completed orders table
    attempts = 0
    while True:
        try:
            completedPage = requests.get(base_path + 'orders/completed_orders', headers= currentHeaders)

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
                completedPage = requests.get(base_path + 'orders/completed_orders?page='+str(each)+'&', headers= currentHeaders)
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
        currentHeaders = doRecaptcha(sellPlayerList, browser,'sell',currentHeaders, False, cardSeriesLink, browser)

    print('DONE EXECUTING SELL ORDERS')
    return currentHeaders



def doRecaptcha(playerLst, webDriver, order, data, doubleCheck, cardSeriesLink, browser):

    if order == 'buy':
        data = Solver(playerLst, webDriver, order, data, doubleCheck, cardSeriesLink, browser)
    else:
        data = Solver(playerLst, webDriver, order, data, doubleCheck, cardSeriesLink, browser)
    
    return data

# the below "Solver" function can be credited to 
# https://github.com/AiWorkshop/Selenium-Project/blob/master/part10-reCaptchaV2.py
def Solver(playerLst, driver, order, data, doubleCheck, cardSeriesLink, browser):
    authList = []
    failedOrderList = []
    readyList = []
    for each in playerLst:
        while True:
            try:
                u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={each['URL']}&json=1&invisible=1"
                r1 = requests.get(u1)
                requestID = int(r1.json().get('request'))
                each['request_id'] = requestID
            except:
                print("FAILED SENDING TOKEN - TRYING AGAIN....")
                continue
            break
    startTime = time.time()
    
    #NEED HEADERS CHECK IN AUTH TOKEN AND AMOUNT FUNCTIONS
    for each in playerLst:
        if order == 'buy':
            attempts = 0
            while True:
                try:
                    authTokenList = getBuyAuthToken(each['URL'], data)
                    each['auth token'] = authTokenList
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
                    orderAmount = getBuyAmount(each['URL'], data)
                    each['buy amount'] = orderAmount
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
        elif order == 'sell':
            attempts = 0
            while True:
                try:
                    authToken = getSellAuthToken(each['URL'], data)
                    each['auth token'] = authToken
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
                    orderAmount = getSellAmount(each['URL'], data)
                    each['sell amount'] = orderAmount
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

    print('--------------------------------------------------------------------------------------------------------------------')
    i = 0
    while i < len(playerLst):

        while True:
            try:
                u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={playerLst[i]['request_id']}&json=1"
                r2 = requests.get(u2)
                if r2.json().get("status") == 1: 
                    form_tokon = r2.json().get("request")
                    playerLst[i]['form_token'] = form_tokon
                    print(f"ACQUIRED TOKEN FOR {playerLst[i]['player name']}")
                    readyList.append(playerLst[i])
                    i += 1
                else:
                    playerLst.append(playerLst.pop(playerLst.index(playerLst[i])))
            except Exception as e:
                print(e)
            break
        
        elapsed_time = time.time() - startTime
        if elapsed_time > 60:
            break

    
    for each in range(0,len(readyList)):
        if order == "buy":
            if doubleCheck:
                print('placing new buy order for ' + readyList[each]['player name'])
            else:
                print(readyList[each]['player name'])
            
            attempts = 0
            while True:
                try:
                    driver.get(readyList[each]['URL'])
                    wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
                    driver.execute_script(wirte_tokon_js)
                    stubsBefore = getStubsAmount(data)
                    data = placeBuyOrder(readyList[each]['URL'], readyList[each]['buy amount'], readyList[each]['form_token'], readyList[each]['auth token'], stubsBefore, data)
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
                print('placing new sell order for ' + playerLst[each]['player name'])
            else:
                print(playerLst[each]['player name'])

            attempts = 0
            while True:
                try:
                    driver.get(readyList[each]['URL'])
                    wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
                    driver.execute_script(wirte_tokon_js)
                    sellableBefore = getTotalSellable(readyList[each]['URL'], data)
                    data = placeSellOrder(readyList[each]['URL'], readyList[each]['sell amount'], readyList[each]['form_token'], readyList[each]['auth token'], sellableBefore, data)

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

    if len(failedOrderList) > 0:
        Solver(failedOrderList, driver, 'sell', data, doubleCheck)

    return data