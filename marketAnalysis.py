from bs4 import BeautifulSoup
import requests
import csv

'''
Program Description: WILL BE ADDED LATER
Program Creator: Justin Nordeman
Date: 08/08/2020
Contact Information: justinnordeman@gmail.com

'''

def getOrders(csvFileArg):
    headers = {
        ''' will be unique to each user '''
    }

    with open(csvFileArg, 'w', newline='', encoding='utf-8') as csv_file:
        packfile = csv.DictWriter(csv_file, fieldnames=['Player Name', 'Order Type', 'Stubs', 'Date'])
        packfile.writeheader()

        #loop through each page
        for x in range(1, 10):
            params = (('page', str(x) + '^'), ('', ''), )
            r = requests.get("https://theshownation.com/mlb20/orders/completed_orders", headers=headers, params = params)

            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find('tbody')
            results = table.find_all('tr')

            
            #loop through each order
            for each in results:

                #get player name
                playerName = each.contents[1].text

                #remove whitespace newline characters
                playerName = playerName.strip()

                #was order bought or sold
                purchaseType = each.contents[3].text.split(' ')[0]

                #remove whitespace newline characters
                purchaseType = purchaseType.strip()

                #find amounts newline characters
                amount = each.contents[3].text.split(' ')[1]

                #remove whitespace and newline characters
                amount = amount.strip()
                amount = amount.replace('\n', "")
                amount = amount.replace('for', "")
                amount = amount.replace(',', "")
                amount = int(amount)


                #find dates
                date = each.contents[5].text

                #write data to CSV file
                packfile.writerow({'Player Name': playerName, 'Order Type': purchaseType, 'Stubs': amount, 'Date': date})
                
        

getOrders('OrderHistory.csv')