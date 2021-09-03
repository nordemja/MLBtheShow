import requests
import traceback
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
from playsound import PlaysoundException, playsound
from requests.api import head
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from anticaptchaofficial.recaptchav3proxyless import recaptchaV3Proxyless

try:
    #header information to authenticate into account

    def getHeaders():
        filename = 'headers.json'
        with open(filename) as f:
            headers = json.load(f)
        return headers

    headers = getHeaders()

    def getStubsAmount(data):
        stubsAmount = requests.get('https://mlb21.theshow.com/dashboard', headers= data)
        soup = BeautifulSoup(stubsAmount.text, 'html.parser')
        stubsAmount = soup.find('div', {'class': 'well stubs'}).text.strip().replace('Stubs Balance\n\n', '').replace(',','').replace('Wallet\n','')
        return int(stubsAmount)

    def getBuyAmount(playerURL, data):
        x = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(x.text, 'html.parser')
        table = soup.find('div', {'class': 'section-open-order-secondary'})
        table = table.find('tbody')
        buyAmount = table.find('tr')
        buyAmount = buyAmount.find_all('td')
        buyAmount = int(buyAmount[1].text.strip().replace(',', ''))
        return buyAmount

    def getSellAmount(playerURL, data):
        x = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(x.text, 'html.parser')
        table = soup.find('div', {'class': 'section-open-order-primary'})
        table = table.find('tbody')
        buyAmount = table.find('tr')
        buyAmount = buyAmount.find_all('td')
        buyAmount = int(buyAmount[1].text.strip().replace(',', ''))
        return buyAmount

    def getBuyAuthToken(playerURL, data):
        pageRequest = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(pageRequest.text, 'html.parser')
        buyForm = soup.find('form', {'id': 'create-buy-order-form'})
        authToken = buyForm.find('input').get('value')
        return authToken

    def getSellAuthToken(playerURL, data):
        pageRequest = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(pageRequest.text, 'html.parser')
        sellForm = soup.find('form', {'id': 'create-sell-order-form'})
        authToken = sellForm.find('input').get('value')
        return authToken

    API_KEY = "d912946a33a658ddf683e126d8551d07"
    data_sitekey = '6Leg5z4aAAAAABNstVp47FWPfKuOWeOtaGDayE6R'

    def doRecaptchaBuy(playerURL, stubsAvail, recaptchaToken, data):
        buyAmount = getBuyAmount(playerURL, data)
        if stubsAvail < buyAmount:
            return 2
        lst = []
        formData = {'authenticity_token': getBuyAuthToken(playerURL, data), 'price': buyAmount + 15, 'g-recaptcha-response': str(recaptchaToken)}
        sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= data)
        print(sendPost)
        lst.append(sendPost)
        return(len(lst))

    def doRecaptchaSell(playerURL, recaptchaToken, data):
        lst = []
        formData = {'authenticity_token': getSellAuthToken(playerURL, data), 'price': getSellAmount(playerURL, data) - 15, 'g-recaptcha-response': str(recaptchaToken)}
        sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= data)
        print(sendPost)
        lst.append
        return(len(lst))

    def Solver(driver, playerURL, order, data):
        u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={playerURL}&json=1&invisible=1"
        r1 = requests.get(u1)
        print(r1.json())
        rid = r1.json().get("request")
        u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
        time.sleep(5)
        while True:
            r2 = requests.get(u2)
            if r2.json().get("status") == 1:
                form_tokon = r2.json().get("request")
                print(r2.json())
                print(type(form_tokon))
                break
            time.sleep(5)
            
        wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
        driver.execute_script(wirte_tokon_js)
        time.sleep(3)
        if order == "buy":
            doRecaptchaBuy(playerURL, getStubsAmount(data), form_tokon, data)
        if order == "sell":
            doRecaptchaSell(playerURL,form_tokon, data)

    def doRecaptcha(playerURL, webDriver, data, order):
        attempts = 0
        while True:
            try:
                webDriver.get(playerURL)
                if order == 'buy':
                    stubsBefore = getStubsAmount(data)
                    placeBuyOrder(playerURL, getStubsAmount(data), data)
                    stubsAfterOrder = getStubsAmount(data)
                    if stubsBefore == stubsAfterOrder:
                        Solver(webDriver, playerURL, "buy", data)
                else:
                    sellableBefore = getTotalSellable(playerURL, data)
                    placeSellOrder(playerURL, data)
                    sellableAfter = getTotalSellable(playerURL, data)
                    if sellableBefore == sellableAfter:
                        Solver(webDriver, playerURL, "sell", data)

            except:
                attempts += 1
                if attempts == 5:
                    playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                    input('Enter new headers in JSON file: ')
                    attempts = 0
                    continue
                continue
            break

    def placeBuyOrder(playerURL, stubsAvail, data):
        buyAmount = getBuyAmount(playerURL, data)
        if stubsAvail < buyAmount:
            return 2
        lst = []
        formData = {'authenticity_token': getBuyAuthToken(playerURL, data), 'price': buyAmount + 15, 'button': ''}
        sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= data)
        print(sendPost)
        lst.append(sendPost)
        return(len(lst))

    def placeSellOrder(playerURL, data):
        lst = []
        formData = {'authenticity_token': getSellAuthToken(playerURL, data), 'price': getSellAmount(playerURL, data) - 15, 'button': ''}
        sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= data)
        print(sendPost)
        lst.append
        return(len(lst))


    def getTotalSellable(playerURL, data):
        playerPage = requests.get(playerURL, headers= data)
        soup = BeautifulSoup(playerPage.text, 'html.parser')
        totalSellable = soup.find('div', {'class': 'section-order-info-secondary'})
        totalSellable = totalSellable.find('div', {'class': 'well'})
        return int(totalSellable.text.strip()[-1])


    def getOpenBuyOrdersList(data):
        buyOrders = []
        openOrdersPage = requests.get('https://mlb21.theshow.com/orders/buy_orders', headers= data)
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
                playerURL = 'https://mlb21.theshow.com' + playerURL['href'].lstrip().rstrip()
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
            openOrdersPage = requests.get('https://mlb21.theshow.com/orders/sell_orders', headers= data)
            soup = BeautifulSoup(openOrdersPage.text, 'html.parser')
            ordersList = soup.find('tbody')
            openOrder = ordersList.find_all('tr')
            for each in openOrder:
                playerDict = {}
                playerName = each.contents[3].text.strip()
                postedPrice = each.contents[5].text.strip().replace(',','')
                orderID = each.get('id')
                playerURL = each.find('a')
                playerURL = 'https://mlb21.theshow.com' + playerURL['href'].lstrip().rstrip()
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
        
        #time.sleep(120)
        print("Executing sell orders....")

        #get data from completed orders table
        attempts = 0
        while True:
            try:
                completedPage = requests.get('https://mlb21.theshow.com/orders/completed_orders', headers= currentHeaders)

                soup = BeautifulSoup(completedPage.text, 'html.parser')
                totalCompletedOrdersPages = soup.find('div', {'class': 'pagination'})
                totalCompletedOrdersPages = totalCompletedOrdersPages.find_all('a')
                totalCompletedOrdersPages =  int(totalCompletedOrdersPages[3].text)
            except:
                attempts += 1
                if attempts == 5:
                    playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                    print(str(getHeaders())+'\n')
                    input('Enter new headers in JSON file: ')
                    currentHeaders = getHeaders()
                    attempts = 0
                    continue
                continue
            break

        for each in range(1, totalCompletedOrdersPages+1):
            print("PAGE: " + str(each))
            cardsSellable = 1
            attempts = 0
            while True:
                try:
                    completedPage = requests.get('https://mlb21.theshow.com/orders/completed_orders?page='+str(each)+'&', headers= currentHeaders)
                    soup = BeautifulSoup(completedPage.text, 'html.parser')
                    playerOrderInfo = soup.find('tbody')
                    playerOrderInfo = playerOrderInfo.find_all('tr')
                except:
                    attempts += 1
                    if attempts == 5:
                        playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                        print(str(getHeaders())+'\n')
                        input('Enter new headers in JSON file: ')
                        currentHeaders = getHeaders()
                        attempts = 0
                        continue
                    continue
                break
            
            for each in playerOrderInfo:
                cardsSellable = 1
                attempts = 0
                while True:
                    try:
                    #loop through completed orders page and get time order was completed as datetime object

                        orderState = 0
                        requestName = each.contents[1].text.strip()
                        orderType = each.contents[3].text.strip().split()[0]
                        if orderType == 'Bought':
                            sellPlayerLink = each.find('a')
                            sellPlayerLink = 'https://mlb21.theshow.com' + sellPlayerLink['href'].lstrip().rstrip()
                            sellableBefore = getTotalSellable(sellPlayerLink, currentHeaders)
                            if sellableBefore > 0:
                                print(requestName)
                                orderState = placeSellOrder(sellPlayerLink, currentHeaders)
                                sellableAfter = getTotalSellable(sellPlayerLink, currentHeaders)
                                print(sellableAfter)
                                if sellableBefore == sellableAfter:
                                    #BROWSER GET
                                    doRecaptcha(sellPlayerLink, browser, currentHeaders, 'sell')
                                    sellableAfter = getTotalSellable(sellPlayerLink, currentHeaders)
                                    if sellableBefore == sellableAfter:
                                        playsound('C:\\Users\\justi\\Downloads\\DingSound.mp3')
                                        input("press enter: ")
                                        
                            else:
                                cardsSellable = 0
                                
            
                    except:
                        attempts += 1
                        if attempts == 5:
                            if orderState == 1:
                                break
                            playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                            print(str(getHeaders())+'\n')
                            input('Enter new headers in JSON file: ')
                            currentHeaders = getHeaders()
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

        print('DONE EXECUTING SELL ORDERS')
        return currentHeaders
        #time.sleep(60)

    print(getStubsAmount(headers))

    chromeOptions = Options()
    chromeOptions.add_extension('C:\\Users\\justi\\Downloads\\Buster Captcha Solver for Humans 1.1.0.0.crx')

    browser = webdriver.Chrome(ChromeDriverManager().install() ,options=chromeOptions)
    browser.get('https://mlb21.theshow.com/community_market')

    time.sleep(5)

    #specify which card series you want to search for

    cardSeriesLink = input('Enter Link of Card Criteria: ')
    cardSeriesBase = 'https://mlb21.theshow.com/community_market'
    cardSeriesFilter = cardSeriesLink.strip(cardSeriesBase+'?page=')

    cardSeries = requests.get(cardSeriesLink, headers = headers)

    #get total pages in card series

    soup = BeautifulSoup(cardSeries.text, 'html.parser')
    totalPagesFound = int(soup.find('h3').text.strip()[-1])
    print(totalPagesFound)
    headers = doSellOrders(headers)
    while True:
        try:
            #blank list of dicts to loop through to place buy order
            openListingLength = len(getTotalOpenOrders(headers))
            listings = []
            
            #loop through each page in search results and get listings from table
            for each in range(1, totalPagesFound+1):
                while True:
                    try:

                        searchReults = requests.get(cardSeriesBase+'?page='+str(each)+cardSeriesFilter+'uipment', headers = headers)
                        soup = BeautifulSoup(searchReults.text, 'html.parser')
                        table = soup.find('tbody')
                        results = table.find_all('tr')

                        #loop through listings pulling needed information to place order then place information in a list of dictionaries
                        for each in results:
                            listingsDict = {}

                            requestName = each.contents[5].text.strip()
                            buyAmount = int(each.contents[11].text.strip()) + 15
                            sellAmount = int(each.contents[9].text.strip()) - 15
                            profit = int((sellAmount) * .9) - buyAmount
                            link = each.find('a')
                            formattedURL = 'https://mlb21.theshow.com' + link['href'].lstrip().rstrip().strip('fave')

                            listingsDict['player name'] = requestName
                            listingsDict['buy amount'] = buyAmount
                            listingsDict['sell amount'] = sellAmount
                            listingsDict['profit'] = profit
                            listingsDict['URL'] = formattedURL
                            listings.append(listingsDict)
                    except:
                        playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                        print(str(getHeaders())+'\n')
                        input('Enter new headers in JSON file: ')
                        headers = getHeaders()
                    break

            #sort by highest profit
            listings = sorted(listings, key = lambda i: i['profit'])
            listings.reverse()  
            
            #place buy order for top 10 most profittable cards
            openOrderList = getTotalOpenOrders(headers)
            currentOpenBuyOrders = len(getOpenBuyOrdersList(headers))
            print('open buy orders = ' , currentOpenBuyOrders)

            for each in listings:
                orderState = 0
                attempts = 0
                while True:
                    try:
                        if any(d['Name'] == each['player name'] for d in openOrderList):
                            print(each['player name'])
                            pass
                        else:
                            print(each)
                            stubsBefore = getStubsAmount(headers)
                            orderState = placeBuyOrder(each['URL'], stubsBefore, headers)
                            if orderState == 2:
                                break
                            else:
                                stubsAfterOrder = getStubsAmount(headers)
                                recaptchaAttempts = 0
                                if stubsBefore == stubsAfterOrder:      
                                    doRecaptcha(each['URL'], browser, headers, 'buy')   
                                    stubsAfterOrder = getStubsAmount(headers)
                                    if stubsBefore == stubsAfterOrder:
                                        playsound('C:\\Users\\justi\\Downloads\\DingSound.mp3')
                                        input("press enter: ")
                                        
                                
                                currentOpenBuyOrders += 1
                                openListingLength += 1
                                print(currentOpenBuyOrders)                 

                    except:
                        attempts += 1
                        if attempts == 5:
                            if orderState == 1:
                                currentOpenBuyOrders += 1
                                openListingLength += 1
                                print(currentOpenBuyOrders)
                                break
                            playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                            print(str(getHeaders())+'\n')
                            input('Enter new headers in JSON file: ')
                            attempts = 0
                            headers = getHeaders()
                            continue
                        else:
                            if orderState == 1:
                                currentOpenBuyOrders += 1
                                openListingLength += 1
                                print(currentOpenBuyOrders)
                                break
                            print("Failed " + str(attempts))
                            continue

                    break
            
                if currentOpenBuyOrders >= 15 or openListingLength >= 25:
                    break
                if orderState == 2:
                    break
                    

            headers = doSellOrders(headers)

            openBuyOrders = getOpenBuyOrdersList(headers)
            browser.get('https://mlb21.theshow.com/orders/buy_orders')
            time.sleep(3)
            for each in openBuyOrders:
                attempts = 0
                while True:
                    try:
                        currentPrice = getBuyAmount(each['URL'], headers)
                    except:
                        attempts += 1
                        if attempts == 5: 
                            playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                            print(str(getHeaders())+'\n')
                            input('Enter new headers in JSON file: ')
                            headers = getHeaders()
                            attempts = 0
                            continue
                        else:
                            print("Failed once")
                            continue
                    break
                
                if int(each['Posted Price']) < currentPrice:
                    while True:
                        try:
                            browser.find_element_by_xpath('//*[@id="'+each['Order ID']+'"]/td[1]/form/button').click()
                            browser.switch_to_alert().accept()
                        except:
                            playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                            print(str(getHeaders())+'\n')
                            input('Enter new headers in JSON file: ')
                            headers = getHeaders()
                        break
                    orderState = 0
                    attempts = 0
                    while True:
                        try:
                            print("posting new order for " + each['Name'])
                            stubsBefore = getStubsAmount(headers)
                            orderState = placeBuyOrder(each['URL'],stubsBefore, headers)
                            if orderState == 2:
                                break
                            stubsAfterOrder = getStubsAmount(headers)
                            recaptchaAttempts = 0
                            if stubsBefore == stubsAfterOrder:
                                doRecaptcha(each['URL'], browser, headers, 'buy')
                                stubsAfterOrder = getStubsAmount(headers)
                                if stubsBefore == stubsAfterOrder:
                                    playsound('C:\\Users\\justi\\Downloads\\DingSound.mp3')
                                    input("press enter: ")

                            browser.get('https://mlb21.theshow.com/orders/buy_orders')
                        except:
                            attempts += 1
                            if attempts == 5:
                                if orderState == 1:
                                    browser.get('https://mlb21.theshow.com/orders/buy_orders')
                                    break
                                playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                                print(str(getHeaders())+'\n')
                                input('Enter new headers in JSON file: ')
                                headers = getHeaders()
                                attempts = 0
                                continue                             
                            else:
                                if orderState == 1:
                                    browser.get('https://mlb21.theshow.com/orders/buy_orders')
                                    break
                                print('Failed ' + str(attempts))
                                continue
                        break
                else:
                    print(each['Name'] + ' at ' + each['Posted Price'] + ' is currently best sell price')
                            
            
            browser.get('https://mlb21.theshow.com/orders/sell_orders')
            time.sleep(5)
            openSellOrders = getOpenSellOrdersList(headers)
            for each in openSellOrders:
                orderState = 0
                attempts = 0
                try:
                    while True:
                        try:
                            currentSellAmount = getSellAmount(each['URL'],headers)
                        except:
                            attempts += 1
                            if attempts == 5:
                                playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                                print(str(getHeaders())+'\n')
                                input('Enter new headers in JSON file: ')
                                headers = getHeaders()
                                attempts = 0
                            else:
                                print("Failed " + str(attempts))
                                continue
                        break
                    if int(each['Posted Price']) > currentSellAmount:
                        print("Cancelling " + each["Name"] + " at " + each["Posted Price"])
                        print(each["Posted Price"])
                        print(currentSellAmount)
                        browser.find_element_by_xpath('//*[@id="'+each["Order ID"]+'"]/td[1]/form/button').click()
                        browser.switch_to_alert().accept()
                        attempts = 0
                        while True:
                            try:
                                sellableBefore = getTotalSellable(each['URL'],headers)
                                orderState = placeSellOrder(each['URL'],headers)
                                sellableAfter = getTotalSellable(each['URL'],headers)
                                recaptchaAttempts = 0
                                if sellableBefore == sellableAfter:
                                    if sellableBefore == 0:
                                        break
                                    doRecaptcha(each['URL'], browser, headers, 'sell')
                                    sellableAfter = getTotalSellable(each['URL'],headers)
                                    if sellableBefore == sellableAfter:
                                        playsound('C:\\Users\\justi\\Downloads\\DingSound.mp3')
                                        input("press enter: ")
                                        break
                                print("NEW SELL ORDER PLACED!")
                            except:
                                attempts += 1
                                if attempts == 5:
                                    if orderState == 1:
                                        break
                                    playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                                    print(str(getHeaders())+'\n')
                                    input('Enter new headers in JSON file: ')
                                    headers = getHeaders()
                                    attempts = 0
                                    continue

                                else:
                                    if orderState == 1:
                                        break
                                    print("failed " + str(attempts))
                                    continue
                            break
                        while True:
                            try:
                                browser.get('https://mlb21.theshow.com/orders/sell_orders')
                            except:
                                attempts += 1
                                if attempts == 5:
                                    playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')
                                    print(str(getHeaders())+'\n')
                                    input('Enter new headers in JSON file: ')
                                    headers = getHeaders()
                                    attempts = 0
                                    continue
                                else:
                                    print("failed " + str(attempts) + " getting open sell page")
                                    continue
                            break
                    else:
                        print(each["Name"] + " at " + each["Posted Price"] + " is currently best buy price")
                except NoSuchElementException:
                    print("Order not found")

                 
            headers = doSellOrders(headers)

        except KeyboardInterrupt:
            print("STOPPING PROGRAM")
            print('CANCELLING ORDERS...')
            break
except Exception:
    print(traceback.format_exc())
    playsound('C:\\Users\\justi\\Downloads\\errorSound.mp3')