from bs4 import BeautifulSoup
import requests

def getTotalSellable(playerURL, data):
    playerPage = requests.get(playerURL, headers= data)
    soup = BeautifulSoup(playerPage.text, 'html.parser')
    totalSellable = soup.find_all('div', {'class': 'well'})[4].text.strip()[-1]
    return int(totalSellable)

def doRecaptchaSell(playerURL, authToken, sellAmount, recaptchaToken, data):
    formData = {'authenticity_token': authToken, 'price': sellAmount - 10, 'g-recaptcha-response': str(recaptchaToken)}
    sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= data)
    print(sendPost)
    return 1

def placeSellOrder(playerURL, sellAmount, form_token, authTokenList, sellableBefore, data):
    i = 0
    if i == 4:
        i = 0
    formData = {'authenticity_token': authTokenList[i], 'price': sellAmount - 10, 'g-recaptcha-response': form_token}
    sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= data)
    sellableAfter = getTotalSellable(playerURL,data)
    while sellableBefore == sellableAfter:
        i += 1
        authToken = authTokenList[i]
        formData = {'authenticity_token': authToken, 'price': sellAmount - 10, 'g-recaptcha-response': form_token}
        sendPost = requests.post(playerURL+'/create_sell_order', formData, headers= data)
        sellableAfter = getTotalSellable(playerURL, data)
    print(sendPost)
    return data