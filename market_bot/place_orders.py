import requests
from amounts import getStubsAmount
from bs4 import BeautifulSoup

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