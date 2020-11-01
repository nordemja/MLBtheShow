import requests
from bs4 import BeautifulSoup
import time

headers = {
    'authority': 'theshownation.com',
    'accept': 'text/html, application/xhtml+xml',
    'turbolinks-referrer': 'https://theshownation.com/mlb20/dashboard',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://theshownation.com/mlb20/dashboard',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ga=GA1.2.231888817.1603072001; tsn_token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTM2MDczLCJ1c2VybmFtZSI6InRocm93YXdheXBpdGNoIiwicGljdHVyZSI6Imh0dHBzOi8vc3RhdGljLXJlc291cmNlLm5wLmNvbW11bml0eS5wbGF5c3RhdGlvbi5uZXQvYXZhdGFyL2RlZmF1bHQvRGVmYXVsdEF2YXRhci5wbmciLCJncm91cHMiOltdfQ.y2fTV0S5wEFoWiVL0aFMHXkpIOyZce4RA9Lk0lOJ_R8; _gid=GA1.2.1505861429.1603719270; _tsn_session=e738e97a98bc96d657844d9e8579f4be; _gat=1',
    'if-none-match': 'W/^\\^c76f73cc4ef15f00301bb836625a677b^\\^',
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

def getBuyOrder(playerURL, price):
    formData = {'authenticity_token': getAuthToken(playerURL), 'price': price, 'button': ''}
    sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= headers)
    print(sendPost)
    print(getStubsAmount())


cardSeries = requests.get('https://theshownation.com/mlb20/community_market?page=2&display_position=&amp=&max_best_buy_price=&max_best_sell_price=&max_rank=&min_best_buy_price=&min_best_sell_price=&min_rank=&name=&player_type_id=&rarity_id=&series_id=10022&team_id=&type=mlb_card', headers = headers)

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

listings = sorted(listings, key = lambda i: i['profit'])
listings.reverse()

for each in range(0,10):
    print(listings[each]['player name'])
    getBuyOrder(listings[each]['URL'], listings[each]['buy amount'])
    time.sleep(25)

'''
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
    if each['best_buy_price'] < (stubsAmount * .1) and each['best_sell_price'] * .9 > 50 and each['best_buy_price'] != 0:
        profit = (int(each['best_sell_price'] * .9 - each['best_buy_price']))
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

        if bestBuyList[i] in range(int(amount)-10,int(amount)+10):
            print(requestName)
            link = each.find('a')
            formatted_url = 'https://theshownation.com' + link['href'].lstrip().rstrip().strip('fave')
            getBuyOrder(testOrderPage)
            time.sleep(25)

    i += 1

lastNames.clear()

'''
'''
x = requests.get('https://theshownation.com/mlb20/community_market?display_position=&amp;max_best_buy_price=&amp;max_best_sell_price=&amp;max_rank=&amp;min_best_buy_price=&amp;min_best_sell_price=&amp;min_rank=&amp;name=&amp;player_type_id=&amp;rarity_id=&amp;series_id=10022&amp;team_id=&amp;type=mlb_card')

for each in results:
        requestName = each.contents[5].text.strip()
        print(requestName)
        link = each.find('a')
        formatted_url = 'https://theshownation.com' + link['href'].lstrip().rstrip().strip('fave')
        getBuyOrder(formatted_url)
        break
    break
'''
