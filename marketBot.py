import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

headers = {
    ''' HEADER INFO GOES HERE --- NOT INCLUDED FOR SECURITY REASONS '''
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
    return buyAmount + 25

def getSellAmount(playerURL):
    x = requests.get(playerURL, headers= headers)
    soup = BeautifulSoup(x.text, 'html.parser')
    table = soup.find('div', {'class': 'section-open-order-primary'})
    table = table.find('tbody')
    buyAmount = table.find('tr')
    buyAmount = buyAmount.find_all('td')
    buyAmount = int(buyAmount[1].text.strip().replace(',', ''))
    return buyAmount - 25

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
    print(getStubsAmount())

def placeSellOrder(playerURL):
    formData = {'authenticity_token': getSellAuthToken(playerURL), 'price': getSellAmount(playerURL), 'button': ''}
    sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= headers)
    print(sendPost)

#get system time
systemTime = datetime.now().strftime("%m/%d/%Y %I:%M%p")

#specify which card series you want to search for
cardSeries = requests.get('https://theshownation.com/mlb20/community_market?page=2&display_position=&amp=&max_best_buy_price=&max_best_sell_price=&max_rank=&min_best_buy_price=&min_best_sell_price=&min_rank=&name=&player_type_id=&rarity_id=&series_id=10022&team_id=&type=mlb_card', headers = headers)

#get total pages in card series
soup = BeautifulSoup(cardSeries.text, 'html.parser')
totalPagesFound = soup.find('h3').text.strip()[-1]
totalPagesFound = int(totalPagesFound)

listings = []
for each in range(1, totalPagesFound+1):
    searchReults = requests.get('https://theshownation.com/mlb20/community_market?page='+str(each)+'&display_position=&amp=&max_best_buy_price=&max_best_sell_price=&max_rank=&min_best_buy_price=&min_best_sell_price=&min_rank=&name=&player_type_id=&rarity_id=&series_id=10022&team_id=&type=mlb_card', headers = headers)
    
    soup = BeautifulSoup(searchReults.text, 'html.parser')
    table = soup.find('tbody')
    results = table.find_all('tr')

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

#place buy order for top 10 cards
for each in range(0,10):
    print(listings[each])
    placeBuyOrder(listings[each]['URL'])
    time.sleep(25)

completedPage = requests.get('https://theshownation.com/mlb20/orders/completed_orders', headers= headers)

soup = BeautifulSoup(completedPage.text, 'html.parser')
playerOrderInfo = soup.find('tbody')
playerOrderInfo = playerOrderInfo.find_all('tr')

systemTime = datetime.strptime(systemTime, "%m/%d/%Y %I:%M%p")
for each in playerOrderInfo:
    requestName = each.contents[1].text.strip()
    timeCompleted = each.contents[5].text.strip().replace(' EDT', '').replace(' EST', '')
    timeCompleted = datetime.strptime(timeCompleted, "%m/%d/%Y %I:%M%p")
    if (timeCompleted > systemTime):
        print(requestName)
        print(timeCompleted)
        sellPlayerLink = each.find('a')
        sellPlayerLink = 'https://theshownation.com' + sellPlayerLink['href'].lstrip().rstrip()
        placeSellOrder(sellPlayerLink)
        time.sleep(25)
print("DONE")