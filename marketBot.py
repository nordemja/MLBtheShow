import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from playsound import playsound

#header information to authenticate into account
headers = {
    ''' HEADER INFORMATION GOES HERE --- NOT INCLUDED FOR SECURITY REASONS '''
}

def getStubsAmount():
    stubsAmount = requests.get('https://theshownation.com/mlb20/dashboard', headers= headers)
    soup = BeautifulSoup(stubsAmount.text, 'html.parser')
    stubsAmount = soup.find('div', {'class': 'well stubs'}).text.strip().replace('Stubs Balance\n\n', '').replace(',','')
    return int(stubsAmount)

def getBuyAmount(playerURL):
    x = requests.get(playerURL, headers= headers)
    soup = BeautifulSoup(x.text, 'html.parser')
    table = soup.find('div', {'class': 'section-open-order-secondary'})
    table = table.find('tbody')
    buyAmount = table.find('tr')
    buyAmount = buyAmount.find_all('td')
    buyAmount = int(buyAmount[1].text.strip().replace(',', ''))
    return buyAmount + 100

def getSellAmount(playerURL):
    x = requests.get(playerURL, headers= headers)
    soup = BeautifulSoup(x.text, 'html.parser')
    table = soup.find('div', {'class': 'section-open-order-primary'})
    table = table.find('tbody')
    buyAmount = table.find('tr')
    buyAmount = buyAmount.find_all('td')
    buyAmount = int(buyAmount[1].text.strip().replace(',', ''))
    return buyAmount - 150

def getBuyAuthToken(playerURL):
    pageRequest = requests.get(playerURL, headers= headers)
    soup = BeautifulSoup(pageRequest.text, 'html.parser')
    buyForm = soup.find('form', {'id': 'create-buy-order-form'})
    authToken = buyForm.find('input').get('value')
    return authToken

def getSellAuthToken(playerURL):
    pageRequest = requests.get(playerURL, headers= headers)
    soup = BeautifulSoup(pageRequest.text, 'html.parser')
    sellForm = soup.find('form', {'id': 'create-sell-order-form'})
    authToken = sellForm.find('input').get('value')
    return authToken

def placeBuyOrder(playerURL):
    formData = {'authenticity_token': getBuyAuthToken(playerURL), 'price': getBuyAmount(playerURL), 'button': ''}
    sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= headers)
    print(sendPost)

def placeSellOrder(playerURL):
    formData = {'authenticity_token': getSellAuthToken(playerURL), 'price': getSellAmount(playerURL), 'button': ''}
    sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= headers)
    print(sendPost)

def getTotalSellable(playerURL):
    playerPage = requests.get(playerURL, headers= headers)
    soup = BeautifulSoup(playerPage.text, 'html.parser')
    totalSellable = soup.find('div', {'class': 'section-order-info-secondary'})
    totalSellable = totalSellable.find('div', {'class': 'well'})
    return int(totalSellable.text.strip()[-1])

def getOpenBuyOrdersList():
    buyOrders = []
    try:
        openOrdersPage = requests.get('https://theshownation.com/mlb20/orders/open_orders', headers= headers)
        soup = BeautifulSoup(openOrdersPage.text, 'html.parser')
        findOrderList = soup.find_all('div', {'class': 'section-block'})

        textList = soup.find_all('h2')
        buyOrderText = textList[1].text
        if buyOrderText in findOrderList[0].text:
            ordersList  = findOrderList[0].find('tbody')
            if ordersList == None:
                return buyOrders
            else:
                openOrder = ordersList.find_all('tr')
                for each in openOrder:
                    playerDict = {}
                    playerName = each.contents[3].text.strip()
                    postedPrice = each.contents[5].text.strip().replace(',','')
                    playerURL = each.find('a')
                    playerURL = 'https://theshownation.com' + playerURL['href'].lstrip().rstrip()
                    playerDict['Name'] = playerName
                    playerDict['Posted Price'] = postedPrice
                    playerDict['URL'] = playerURL
                    buyOrders.append(playerDict)

    except AttributeError:
        print("Attribute Error")

    return buyOrders

def getOpenSellOrdersList():
    sellOrders = []
    try:
        openOrdersPage = requests.get('https://theshownation.com/mlb20/orders/open_orders', headers= headers)
        soup = BeautifulSoup(openOrdersPage.text, 'html.parser')
        findOrderList = soup.find_all('div', {'class': 'section-block'})

        textList = soup.find_all('h2')
        buyOrderText = textList[1].text
        if buyOrderText in findOrderList[0].text:
            ordersList  = findOrderList[1].find('tbody')
            if ordersList == None:
                return sellOrders
            else:
                openOrder = ordersList.find_all('tr')
                for each in openOrder:
                    playerDict = {}
                    playerName = each.contents[3].text.strip()
                    postedPrice = each.contents[5].text.strip().replace(',','')
                    playerURL = each.find('a')
                    playerURL = 'https://theshownation.com' + playerURL['href'].lstrip().rstrip()
                    playerDict['Name'] = playerName
                    playerDict['Posted Price'] = postedPrice
                    playerDict['URL'] = playerURL
                    sellOrders.append(playerDict)

    except AttributeError:
        print("Attribute Error")
    
    return sellOrders

def getTotalOpenOrders():
    buyOrderList = getOpenBuyOrdersList()
    sellOrderList = getOpenSellOrdersList()
    return buyOrderList + sellOrderList

#get system time
systemTime = datetime.now().strftime("%m/%d/%Y %I:%M%p")
systemTime = datetime.strptime(systemTime, "%m/%d/%Y %I:%M%p")

#specify which card series you want to search for

cardSeries = requests.get('https://theshownation.com/mlb20/community_market?page=1&display_position=&amp=&max_best_buy_price=&max_best_sell_price=&max_rank=&min_best_buy_price=&min_best_sell_price=&min_rank=&name=&player_type_id=&rarity_id=&series_id=10022&team_id=&type=mlb_card', headers = headers)

#get total pages in card series
soup = BeautifulSoup(cardSeries.text, 'html.parser')
totalPagesFound = int(soup.find('h3').text.strip()[-1])

while True:
    try:
        #blank list of dicts to loop through to place buy order
        listings = []

        #loop through each page in search results and get listings from table
        for each in range(1, totalPagesFound+1):
            searchReults = requests.get('https://theshownation.com/mlb20/community_market?page='+str(each)+'&display_position=&amp=&max_best_buy_price=&max_best_sell_price=&max_rank=&min_best_buy_price=&min_best_sell_price=&min_rank=&name=&player_type_id=&rarity_id=&series_id=10022&team_id=&type=mlb_card', headers = headers)
            
            soup = BeautifulSoup(searchReults.text, 'html.parser')
            table = soup.find('tbody')
            results = table.find_all('tr')

            #loop through listings pulling needed information to place order then place information in a list of dictionaries
            for each in results:
                listingsDict = {}

                requestName = each.contents[5].text.strip()
                buyAmount = int(each.contents[11].text.strip()) +1
                sellAmount = int(each.contents[9].text.strip()) -1
                profit = int((sellAmount - 1) * .9) - buyAmount +1
                link = each.find('a')
                formattedURL = 'https://theshownation.com' + link['href'].lstrip().rstrip().strip('fave')

                listingsDict['player name'] = requestName
                listingsDict['buy amount'] = buyAmount
                listingsDict['sell amount'] = sellAmount
                listingsDict['profit'] = profit
                listingsDict['URL'] = formattedURL
                listings.append(listingsDict)

        #sort by highest profit
        listings = sorted(listings, key = lambda i: i['profit'])
        listings.reverse()

        #place buy order for top 10 most profittable cards
        openOrderList = getTotalOpenOrders()
        currentOpenBuyOrders = len(getOpenBuyOrdersList())
        print('open buy orders = ' , currentOpenBuyOrders)
        print(openOrderList)

        for each in listings:

            try:
                if any(d['Name'] == each['player name'] for d in openOrderList):
                    print(each['player name'])
                    pass
                else:
                    print(each)
                    stubsBefore = getStubsAmount()
                    placeBuyOrder(each['URL'])
                    stubsAfterOrder = getStubsAmount()

                    while (stubsBefore == stubsAfterOrder):
                        playsound('C:\\Users\\justi\\Downloads\\DingSound.mp3')
                        input("press button to continue: ")
                        print(each)
                        stubsBefore = getStubsAmount()
                        placeBuyOrder(each['URL'])
                        stubsAfterOrder = getStubsAmount()
        

                    currentOpenBuyOrders += 1
                    print(currentOpenBuyOrders)
                
                    if currentOpenBuyOrders == 10:
                        break

            except AttributeError:
                print('FAILED')

        print('sleeping...')
        time.sleep(120)
        print('executing sell orders...')

        #get data from completed orders table
        completedPage = requests.get('https://theshownation.com/mlb20/orders/completed_orders', headers= headers)

        soup = BeautifulSoup(completedPage.text, 'html.parser')
        totalCompletedOrdersPages = soup.find('div', {'class': 'pagination'})
        totalCompletedOrdersPages = totalCompletedOrdersPages.find_all('a')
        totalCompletedOrdersPages =  int(totalCompletedOrdersPages[3].text)

        for each in range(1, totalCompletedOrdersPages+1):
            test = 'https://theshownation.com/mlb20/orders/completed_orders?page='+str(each)
            completedPage = requests.get('https://theshownation.com/mlb20/orders/completed_orders?page='+str(each)+'&', headers= headers)

            soup = BeautifulSoup(completedPage.text, 'html.parser')
            playerOrderInfo = soup.find('tbody')
            playerOrderInfo = playerOrderInfo.find_all('tr')

            #loop through completed orders page and get time order was completed as datetime object
            for each in playerOrderInfo:
                requestName = each.contents[1].text.strip()
                orderType = each.contents[3].text.strip().split()[0]
                if orderType == 'Bought':
                    sellPlayerLink = each.find('a')
                    sellPlayerLink = 'https://theshownation.com' + sellPlayerLink['href'].lstrip().rstrip()
                    totalSellable = getTotalSellable(sellPlayerLink)
                    if totalSellable > 0:
                        sellableBefore = getTotalSellable(sellPlayerLink)
                        placeSellOrder(sellPlayerLink)
                        sellableAfter = getTotalSellable(sellPlayerLink)
                        print(requestName)
                        print(sellableAfter)
                        while sellableBefore == sellableAfter:
                            playsound('C:\\Users\\justi\\Downloads\\DingSound.mp3')
                            input("press button to continue: ")
                            print(requestName)
                            placeSellOrder(sellPlayerLink)
                            sellableAfter = getTotalSellable(sellPlayerLink)
                        #currentOpenBuyOrders -= 1
                        #print(currentOpenBuyOrders)
                        nextPage = True
                    else:
                        nextPage = False
                        break

            if nextPage == False:
                break

        print('DONE EXECUTING SELL ORDERS')
        time.sleep(60)

        openSellOrders = getOpenSellOrdersList()
        for each in openSellOrders:
            currentSellAmount = getSellAmount(each['URL'])
            if int(each['Posted Price']) > currentSellAmount:
                input('cancel order: ' + each['Name'] + ':' + ' '+ each['Posted Price'])
                print(each)
                sellableBefore = getTotalSellable(each['URL'])
                placeSellOrder(each['URL'])
                sellableAfter = getTotalSellable(each['URL'])
                while sellableBefore == sellableAfter:
                    playsound('C:\\Users\\justi\\Downloads\\DingSound.mp3')
                    input("press button to continue: ")
                    print(each['Name'])
                    placeSellOrder(each['URL'])
                    sellableAfter = getTotalSellable(each['URL'])



    except KeyboardInterrupt:
        print("STOPPING PROGRAM")
        break            