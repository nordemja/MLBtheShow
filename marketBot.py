import requests
from bs4 import BeautifulSoup

headers = {

'''HEADER INFO GOES HERE'''
}

def getStubsAmount():
    stubsAmount = requests.get('https://theshownation.com/mlb20/dashboard', headers= headers)
    soup = BeautifulSoup(stubsAmount.text, 'html.parser')
    stubsAmount = soup.find('div', {'class': 'well stubs'}).text.strip().replace('Stubs Balance\n\n', '').replace(',','')
    return int(stubsAmount)

def getAuthToken(playerURL):
        r = requests.get(playerURL, headers= headers)
        pagetext = r.text
        soup = BeautifulSoup(pagetext, 'html.parser')
        inventory = soup.find('div', {'class': 'market-forms-price'})
        buyForm = inventory.find('form', {'id': 'create-buy-order-form'})
        authToken = buyForm.find('input').get('value')
        return authToken

def getBuyOrder(playerURL):
    formData = {'authenticity_token': getAuthToken(playerURL), 'price': '101', 'button': ''}
    sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= headers)
    print(sendPost)
    print(getStubsAmount())


#page = 'https://theshownation.com/mlb20/items/fffffe98d0963d27015c198262d97221'
#getBuyOrder(page)


#get initial API results to get total number of pages and set variable to total pages
page = requests.get('https://theshownation.com/mlb20/apis/listings.json?type=mlb_card&page=1')
listingsDict = page.json()
totalPages = listingsDict["total_pages"]

cumalitiveListing = []
stubsAmount = getStubsAmount()


#looop through all API pages and add to list that will be in alphabetical order
for each in range(1,totalPages+1):
    temp = requests.get('https://theshownation.com/mlb20/apis/listings.json?type=mlb_card&page=' + str(each)).json()
    
    for each in temp["listings"]:
        cumalitiveListing.append(each)

#new list to add profits of results fitting criteria
filteredProfitList = []

#loop through each listed item
for each in cumalitiveListing:

    #set criteria, calculate profit, and add to filteredProfitList
    if each['best_buy_price'] < (stubsAmount * .25) and each['best_sell_price'] * .9 > 50 and each['best_buy_price'] != 0:
        profit = (int(each['best_sell_price'] * .9 - each['best_buy_price']))
        if profit < 900:
            each['profit'] = profit
            filteredProfitList.append(each)

#clear initial list to save memory
cumalitiveListing.clear()

#sort filteredProfitList from most profitable to least profitable
filteredProfitList = sorted(filteredProfitList, key = lambda i: i['profit'])
filteredProfitList.reverse()

#take last name of top 10 profitable cards and append to new list
lastNames = []
bestBuyList = []
for each in range (0,10):
    topTenDict = filteredProfitList[each]
    print(topTenDict)
    bestBuyList.append(topTenDict['best_buy_price'])
    lastNames.append(topTenDict['name'].split()[-1])


filteredProfitList.clear()

i = 0
for each in lastNames:
    searchReults = requests.get('https://theshownation.com/mlb20/community_market?display_position=&amp;max_best_buy_price=&amp;max_best_sell_price=&amp;max_rank=&amp;min_best_buy_price=&amp;min_best_sell_price=&amp;min_rank=&amp;name='+each+'&amp;player_type_id=&amp;rarity_id=&amp;series_id=&amp;team_id=&amp;type=mlb_card', headers = headers)

    soup = BeautifulSoup(searchReults.text, 'html.parser')
    table = soup.find('tbody')
    results = table.find_all('tr')

    for each in results:
        requestName = each.contents[5].text.strip()
        amount = each.contents[11].text.strip()
        if int(amount) == bestBuyList[i]:
            print(requestName)
            print(amount)

            link = each.find('a')
            formatted_url = 'https://theshownation.com' + link['href'].lstrip().rstrip().strip('fave')
            print(formatted_url)
            
            print(getAuthToken(formatted_url))

    i += 1

lastNames.clear()