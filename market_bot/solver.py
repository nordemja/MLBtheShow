# the below "Solver" function can be credited to 
# https://github.com/AiWorkshop/Selenium-Project/blob/master/part10-reCaptchaV2.py

def Solver(playerLst, driver, order, data, doubleCheck):
        authList = []
        failedOrderList = []
        for each in playerLst:
            while True:
                try:
                    u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={each['URL']}&json=1&invisible=1"
                    r1 = s.get(u1)
                    requestID = int(r1.json().get('request'))
                    each['request_id'] = requestID
                except:
                    print("FAILED SENDING TOKEN - TRYING AGAIN....")
                    continue
                break
        startTime = time.time()
        
        #NEED HEADERS CHECK IN AUTH TOKEN AND AMOUNT FUNCTIONS
        for each in playerLst:
            if order == 'buy':
                attempts = 0
                while True:
                    try:
                        authToken = getBuyAuthToken(each['URL'], data)
                        authToken = authToken[1]
                        each['auth token'] = authToken
                    except:
                        attempts += 1
                        if attempts == 5:
                            playsound(error_sound_path)
                            print(str(get_headers())+'\n')
                            input('Enter new headers in JSON file 1: ')
                            attempts = 0
                            data = get_headers()
                            continue
                    break
                
                attempts = 0
                while True:
                    try:
                        orderAmount = getBuyAmount(each['URL'], data)
                        each['buy amount'] = orderAmount
                    except:
                        attempts += 1
                        if attempts == 5:
                            playsound(error_sound_path)
                            print(str(get_headers())+'\n')
                            input('Enter new headers in JSON file 2: ')
                            attempts = 0
                            data = get_headers()
                            continue
                    break
            elif order == 'sell':
                attempts = 0
                while True:
                    try:
                        authToken = getSellAuthToken(each['URL'], data)
                        authList.append(authToken)
                    except:
                        attempts += 1
                        if attempts == 5:
                            playsound(error_sound_path)
                            print(str(get_headers())+'\n')
                            input('Enter new headers in JSON file 3: ')
                            attempts = 0
                            data = get_headers()
                            continue
                    break
                
                attempts = 0
                while True:
                    try:
                        orderAmount = getSellAmount(each['URL'], data)
                        each['sell amount'] = orderAmount
                    except:
                        attempts += 1
                        if attempts == 5:
                            playsound(error_sound_path)
                            print(str(get_headers())+'\n')
                            input('Enter new headers in JSON file 4: ')
                            attempts = 0
                            data = get_headers()
                            continue
                    break

        print('--------------------------------------------------------------------------------------------------------------------')
        i = 0
        while i <= 9:

            while True:
                try:
                    u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={playerLst[i]['request_id']}&json=1"
                    r2 = s.get(u2)
                    if r2.json().get("status") == 1: 
                        id_val = playerLst[i]['request_id']
                        form_tokon = r2.json().get("request")
                        playerLst[i]['form_token'] = form_tokon
                        print(f"ACQUIRED TOKEN FOR {playerLst[i]['player name']}")
                        i += 1
                    else:
                        #print(f"Token for {each['player name']} not ready yet")
                        playerLst.append(playerLst.pop(playerLst.index(playerLst[i])))
                except Exception as e:
                    print(e)
                break
            
            elapsed_time = time.time() - startTime
            if elapsed_time > 60:
                break

        
        for each in range(0,len(playerLst)):
            if order == "buy":
                if doubleCheck:
                    print('placing new buy order for ' + playerLst[each]['player name'])
                else:
                    print(playerLst[each]['player name'])
                
                attempts = 0
                while True:
                    try:
                        driver.get(playerLst[each]['URL'])
                        time.sleep(2)
                        
                        wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
                        driver.execute_script(wirte_tokon_js)
                        stubsBefore = getStubsAmount(data)
                        # authToken = authList[each]
                        data = placeBuyOrder(playerLst[each]['URL'], playerLst[each]['buy amount'], playerLst[each]['form_token'], playerLst[each]['auth token'], stubsBefore, data)
                    except:
                        attempts += 1
                        if attempts == 5:
                            playsound(error_sound_path)
                            print(str(get_headers())+'\n')
                            input('Enter new headers in JSON file 5: ')
                            attempts = 0
                            data = get_headers()
                            continue
                    break

            if order == "sell":
                if doubleCheck:
                    print('placing new sell order for ' + playerLst[each]['player name'])
                else:
                    print(playerLst[each]['player name'])
                attempts = 0
                while True:
                    try:
                        sellableBefore = getTotalSellable(playerLst[each]['URL'], data)
                        authToken = authList[each]
                        data = placeSellOrder(playerLst[each]['URL'], playerLst[each]['sell amount'], tokenList[each], authToken, sellableBefore, data)

                    except:
                        attempts += 1
                        if attempts == 5:
                            playsound(error_sound_path)
                            print(str(get_headers())+'\n')
                            input('Enter new headers in JSON file 6: ')
                            attempts = 0
                            data = get_headers()
                        continue
                    break

        if len(failedOrderList) > 0:
            Solver(failedOrderList, driver, 'sell', data, doubleCheck)

        return data