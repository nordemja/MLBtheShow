from bs4 import BeautifulSoup
import requests
import csv
import uuid





def getOrders():

    headers = {
        'authority': 'theshownation.com',
        'accept': 'text/html, application/xhtml+xml',
        'turbolinks-referrer': 'https://theshownation.com/mlb20/orders/completed_orders',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://theshownation.com/mlb20/orders/completed_orders',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'tsn_token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NDQ1MDgsInVzZXJuYW1lIjoiQ2luY3lGYW42MiIsInBpY3R1cmUiOiJodHRwczovL3N0YXRpYy1yZXNvdXJjZS5ucC5jb21tdW5pdHkucGxheXN0YXRpb24ubmV0L2F2YXRhci9XV1NfRS9FMDAyMC5wbmciLCJncm91cHMiOltdfQ.xPGBL5SKPRuBrAeQbjgbfqXxzEaispOVyLho_tgX4Ys; _ga=GA1.2.450579444.1594916795; tsn_last_seen_notification_id=98957295; _gid=GA1.2.650183171.1596406452; _tsn_session=881eb4e15c2a23530b4d4c2e12e4e2b8; tsn_last_seen_roster_id=10; _gat=1',
        'if-none-match': 'W/^\\^54dae3916610e5e8f3928e32d9999a0f^\\^', 
        }


    for x in range(1, 2):
        params = (('page', str(x) + '^'), ('', ''), )
        r = requests.get("https://theshownation.com/mlb20/orders/completed_orders", headers=headers, params = params)
        print(r.url)

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('tbody')
        results = table.find_all('tr')

        for each in results:
            playerName = each.find('a').text
            print(playerName)

getOrders()