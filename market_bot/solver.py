import requests
import time
from main import API_KEY, data_sitekey, error_sound_path
from auth_token import getBuyAuthToken, getSellAuthToken
from tools import get_new_browser_session
from headers import create_new_headers, get_headers
from amounts import getBuyAmount, getSellAmount, getStubsAmount
from place_orders import getTotalSellable, placeBuyOrder, placeSellOrder
from playsound import playsound


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