import requests
from amounts import getStubsAmount
from headers import get_headers, create_new_headers
from tools import get_new_browser_session
from get_total_sellable import getTotalSellable
from playsound import playsound

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
        if sellableAfter == 0:
                print(sellableAfter)
                print('i = ' + str(authTokenList.index(each)))
                print("length of authToken = " +str(len(authTokenList)))
                print(sendPost)
                break
          
    print(sellableAfter)
    print("ORDER NOT PLACED !!!")

    return data