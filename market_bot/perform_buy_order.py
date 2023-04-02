def doRecaptchaBuy(playerURL, authToken, buyAmount, recaptchaToken, data):
    formData = {'authenticity_token': authToken, 'price': buyAmount + 10, 'g-recaptcha-response': str(recaptchaToken)}
    sendPost = s.post(playerURL+'/create_buy_order', formData, headers= data)
    print(sendPost)
    return 1

def placeBuyOrder(playerURL, buyAmount, form_token, authToken, stubsBefore, data):
    i = 0
    formData = {'authenticity_token': authToken, 'price': buyAmount + 10, 'g-recaptcha-response': form_token}
    sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= data)
    stubsAfter = getStubsAmount(data)
    while stubsBefore == stubsAfter:
        i += 1
        if i == 4:
            i = 0
        formData = {'authenticity_token': authToken, 'price': buyAmount + 10, 'g-recaptcha-response': form_token}
        sendPost = requests.post(playerURL+'/create_buy_order', formData, headers= data)
        stubsAfter = getStubsAmount(data)
    print(sendPost)
    return data