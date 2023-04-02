def getStubsAmount(data):
    stubsAmount = s.get(base_path + 'dashboard', headers= data)
    soup = BeautifulSoup(stubsAmount.text, 'html.parser')
    stubsAmount = soup.find('div', {'class': 'well stubs'}).text.strip().replace('Stubs Balance\n\n', '').replace(',','').replace('Wallet\n','')
    return int(stubsAmount)

def getBuyAmount(playerURL, data):
    x = s.get(playerURL, headers= data)
    soup = BeautifulSoup(x.text, 'html.parser')
    buyAmount = int(soup.find('input', {'name': 'price'}).get('value'))
    return buyAmount

def getSellAmount(playerURL, data):
    x = s.get(playerURL, headers= data)
    soup = BeautifulSoup(x.text, 'html.parser')
    sellAmount = soup.find_all('input', {'name': 'price'})
    sellAmount = int(sellAmount[0].get('value'))
    return sellAmount