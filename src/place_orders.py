import requests
from amounts import getStubsAmount
from headers import get_headers, create_new_headers
from tools import get_new_browser_session
from get_total_sellable import getTotalSellable
from playsound import playsound


def place_buy_order(playerURL, buyAmount, form_token, authToken, stubsBefore, data):

    for each in authToken:
        form_data = {
            "authenticity_token": each,
            "price": buyAmount + 25,
            "g-recaptcha-response": form_token,
        }
        send_post = requests.post(
            playerURL + "/create_buy_order", form_data, headers=data
        )

    stubs_after = getStubsAmount(data)
    if stubsBefore != stubs_after:
        # print('i = ' + str(authToken.index(each)))
        # print("length of authToken = " +str(len(authToken)))
        print(send_post)

    else:
        print("ORDER NOT PLACED")

    return data


def place_sell_order(
    playerURL, sellAmount, form_token, authTokenList, sellableBefore, data
):
    for each in authTokenList:
        form_data = {
            "authenticity_token": each,
            "price": sellAmount - 25,
            "g-recaptcha-response": form_token,
        }
        send_post = requests.post(
            playerURL + "/create_sell_order", form_data, headers=data
        )

    sellable_after = getTotalSellable(playerURL, data)

    if sellable_after != sellableBefore:
        print(sellable_after)
        # print('i = ' + str(authTokenList.index(each)))
        # print("length of authToken = " +str(len(authTokenList)))
        print(send_post)

    else:
        sellable_after == sellableBefore
        print(sellable_after)
        print("ORDER NOT PLACED")

    return data
