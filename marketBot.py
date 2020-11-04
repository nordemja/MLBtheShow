import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

#header information to authenticate into account
headers = {

''' HEADER INFO TO AUTHENTICATE IN GOES HERE --- NOT INCLUDED FOR SECURITY REASONS '''
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

def placeBuyOrdersForList(playerInfoDict):
    print(playerInfoDict)
    placeBuyOrder(playerInfoDict['URL'])
    stubsAfter = getStubsAmount()
    return stubsAfter

def getTotalSellable(playerURL):
    playerPage = requests.get(playerURL, headers= headers)
    soup = BeautifulSoup(playerPage.text, 'html.parser')
    totalSellable = soup.find('div', {'class': 'section-order-info-secondary'})
    totalSellable = totalSellable.find('div', {'class': 'well'})
    return int(totalSellable.text.strip()[-1])

def loopThroughToBuyList(buyList, openSellList, buyOrdersOpen):
    for each in buyList:

        try:
            if buyList[0]['player name'] in openSellList:
                print(buyList[0]['player name'])
                pass
            else:
                stubsBefore = getStubsAmount()
                stubsAfterOrder = placeBuyOrdersForList(buyList[0])

                while (stubsBefore == stubsAfterOrder):
                    input("press button to continue: ")
                    stubsBefore = getStubsAmount()
                    stubsAfterOrder= placeBuyOrdersForList(buyList[0])

                buyOrdersOpen += 1
                statusCode = "proceed"
                buyList.pop(0)
                print(buyOrdersOpen)
            
                if buyOrdersOpen == 10:
                    break

        except AttributeError:
            statusCode = 'failed'
            #function(listings, openPlayerSellList)

def getOpenBuyOrders():
    openPlayerBuyList = []
    try:
        openOrdersPage = requests.get('https://theshownation.com/mlb20/orders/open_orders', headers= headers)
        soup = BeautifulSoup(openOrdersPage.text, 'html.parser')
        openSellOrders = soup.find('tbody')
        openPlayerSells = openSellOrders.find_all('tr')

        for each in openPlayerSells:
            #orderID = each.get('id').replace('sell-order-', '')
            playerLink = each.find('a')
            openPlayerBuyList.append(playerLink.text)
    except AttributeError:
        openPlayerBuyList 

    return openPlayerBuyList


def getOpenSellOrders():
    openPlayerBuyList = []
    try:
        openOrdersPage = requests.get('https://theshownation.com/mlb20/orders/open_orders', headers= headers)
        soup = BeautifulSoup(openOrdersPage.text, 'html.parser')
        openSellOrders = soup.find_all('tbody')[1]
        openPlayerSells = openSellOrders.find_all('tr')

        for each in openPlayerSells:
            #orderID = each.get('id').replace('sell-order-', '')
            playerLink = each.find('a')
            openPlayerBuyList.append(playerLink.text)
    except AttributeError:
        openPlayerBuyList 

    return openPlayerBuyList

print(getOpenBuyOrders())   
print(getOpenSellOrders())
'''
#get system time
systemTime = datetime.now().strftime("%m/%d/%Y %I:%M%p")
systemTime = datetime.strptime(systemTime, "%m/%d/%Y %I:%M%p")
print(systemTime)

#specify which card series you want to search for
cardSeries = requests.get('https://theshownation.com/mlb20/community_market?page=2&display_position=&amp=&max_best_buy_price=&max_best_sell_price=&max_rank=&min_best_buy_price=&min_best_sell_price=&min_rank=&name=&player_type_id=&rarity_id=&series_id=10022&team_id=&type=mlb_card', headers = headers)

#get total pages in card series
soup = BeautifulSoup(cardSeries.text, 'html.parser')
totalPagesFound = soup.find('h3').text.strip()[-1]
totalPagesFound = int(totalPagesFound)

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

#openPlayerSellList = getOpenSellOrders()
#print(openPlayerSellList)

#place buy order for top 10 most profittable cards
openPlayerSellList = []
ordersPlaced = 0
loopThroughToBuyList(listings, openPlayerSellList, ordersPlaced)
#function(toBuyList, currentOpenSells)

            
        
print('sleeping...')
time.sleep(120)
print('executing sell orders...')


#get data from completed orders table
completedPage = requests.get('https://theshownation.com/mlb20/orders/completed_orders', headers= headers)

soup = BeautifulSoup(completedPage.text, 'html.parser')
playerOrderInfo = soup.find('tbody')
playerOrderInfo = playerOrderInfo.find_all('tr')

#loop through completed orders page and get time order was completed as datetime object
for each in playerOrderInfo:
    requestName = each.contents[1].text.strip()
    timeCompleted = each.contents[5].text.strip().replace(' EDT', '').replace(' EST', '')
    timeCompleted = datetime.strptime(timeCompleted, "%m/%d/%Y %I:%M%p")
    orderType = each.contents[3].text.strip().split()[0]


    #place sell order if bought after recorded systemTime
    if (timeCompleted >= systemTime and orderType == 'Bought'):
        print(requestName)
        print(timeCompleted)
        sellPlayerLink = each.find('a')
        sellPlayerLink = 'https://theshownation.com' + sellPlayerLink['href'].lstrip().rstrip()
        sellableBefore = getTotalSellable(sellPlayerLink)
        placeSellOrder(sellPlayerLink)
        sellableAfter = getTotalSellable(sellPlayerLink)
        print(sellableAfter)
        while sellableBefore == sellableAfter:
            input("press button to continue: ")
            print(requestName)
            placeSellOrder(sellPlayerLink)
            sellableAfter = getTotalSellable(sellPlayerLink)
        ordersPlaced -= 1
        print(ordersPlaced)


openOrdersPage = requests.get('https://theshownation.com/mlb20/orders/open_orders', headers= headers)
soup = BeautifulSoup(openOrdersPage.text, 'html.parser')
openSellOrders = soup.find('tbody')
openPlayerSells = openSellOrders.find_all('tr')

for each in openPlayerSells:

    orderID = each.get('id').replace('sell-order-', '')
    playerLink = each.find('a')
    openPlayerSellList.append(playerLink.text)
    playerLink = 'https://theshownation.com' + playerLink['href'].lstrip().rstrip()
    orderPrice = int(each.contents[5].text.strip().replace(',',''))
'''
'''
    currentSellPrice  = getSellAmount(playerLink)


    if (orderPrice > currentSellPrice):

        cancelData = {'order_id': orderID, 'type': 'sell'}
        cancelLink = playerLink + '/cancel?order_id=' + orderID + '&type=sell'
        cancelRequest = requests.post(cancelLink, cancelData, headers= headers)
        print(cancelData['order_id'])
        print(cancelRequest)
'''