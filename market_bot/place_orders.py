import requests
from amounts import getStubsAmount
from headers import get_headers, create_new_headers
from tools import get_new_browser_session
from solver import doRecaptcha
from bs4 import BeautifulSoup
from playsound import playsound
from main import base_path, error_sound_path

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
        currentHeaders = doRecaptcha(sellPlayerList, browser,'sell',currentHeaders, False)

    print('DONE EXECUTING SELL ORDERS')
    return currentHeaders

def getTotalSellable(playerURL, data):
    try:
        playerPage = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(playerPage.text, 'html.parser')
        totalSellable = soup.find_all('div', {'class': 'well'})[4].text.strip()[-1]
        return int(totalSellable)
    except Exception as e:
        print(e)

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