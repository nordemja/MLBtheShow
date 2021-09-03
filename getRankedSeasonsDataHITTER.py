import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import time
import csv
import pandas as pd


headers =  {
    'authority': 'mlb21.theshow.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://mlb21.theshow.com/community_market',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'tsn_token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MjEzNjM2LCJ1c2VybmFtZSI6ImFuZ3J5X3BsYXR5cHVzNjJfUFNOIiwicGljdHVyZSI6Imh0dHBzOi8vdGhlc2hvd25hdGlvbi1wcm9kdWN0aW9uLnMzLmFtYXpvbmF3cy5jb20vZm9ydW1faWNvbnMvaWNvbl9jb29wX3dvcmxkc2VyaWVzLnBuZyIsImdyb3VwcyI6W119.6MEixvbrWIrlEMIkCykXZ595vvxs9EDowOIX2WXR3qA; ab.storage.userId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5=^%^7B^%^22g^%^22^%^3A^%^225704733^%^22^%^2C^%^22c^%^22^%^3A1628521772020^%^2C^%^22l^%^22^%^3A1628521772020^%^7D; ab.storage.deviceId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5=^%^7B^%^22g^%^22^%^3A^%^2204839285-6d34-b9e7-e1e0-431013c2293e^%^22^%^2C^%^22c^%^22^%^3A1628521772022^%^2C^%^22l^%^22^%^3A1628521772022^%^7D; _ga=GA1.2.542046081.1628521162; _ga_EJKYYHZPBF=GS1.1.1628560893.2.1.1628560901.0; _gid=GA1.2.382135078.1629056049; tsn_last_url=--CCFFYHBDZE06TDQk68hMVBcSZuvvw5UCRzitOjbSApfN2rN_okCOAOd_nyy4rT; _tsn_session=e597f26164d2ea4b0ef34ef38105bbdc; ab.storage.sessionId.bbce52ad-c4ca-45bc-9c03-b1183aff5ee5=^%^7B^%^22g^%^22^%^3A^%^2200afd509-3216-ce4a-132b-76436e181a16^%^22^%^2C^%^22e^%^22^%^3A1629144620462^%^2C^%^22c^%^22^%^3A1629142820463^%^2C^%^22l^%^22^%^3A1629142820463^%^7D',
    'if-none-match': 'W/^\\^923e7cf80fcf542c9553423ecac886c3^\\^',
}


getProfile = requests.get('https://mlb21.theshow.com/universal_profiles/angry_platypus62/game_history?mode=ARENA', headers=headers)
soup = BeautifulSoup(getProfile.text, 'html.parser')

totalPages = soup.find('div', {'class': 'pagination'})
totalPages = totalPages.find_all('a')
totalPages =  int(totalPages[3].text)
print(totalPages)

with open('C:\\Users\\justi\\OneDrive\\Documents\\Python Programming\\MLBtheShow\\rankedSeasonsStatsHITTER.csv', 'w', newline='', encoding='utf-8') as csvFile:
    statsFile = csv.DictWriter(csvFile, fieldnames=['Date','Stadium','Lineup', 'Position', 'Player', 'AB', 'R', 'H', 'RBI', 'BB', 'SO', 'AVG'])
    statsFile.writeheader()
    for x in range(1, totalPages+1):
        while True:
            try:
                print("page: " +str(x))
                getProfile = requests.get('https://mlb21.theshow.com/universal_profiles/angry_platypus62/game_history?page='+str(x)+'&mode=ARENA', headers=headers)
                soup = BeautifulSoup(getProfile.text, 'html.parser')
                getGames = soup.findAll('div', {'class': 'mlb21-games-box'})
            except:
                input("press enter: ")
                continue
            break

        for each in getGames:
            while True:
                try:
                    url = each.findAll('a')
                    url = url[-1]
                    url =  'https://mlb21.theshow.com' + url['href']
                    onlineMatch = requests.get(url, headers=headers)
                    soup = BeautifulSoup(onlineMatch.text, 'html.parser')
                    onlineMatch = soup.find('div', {'class': 'section-block'})
                    onlineMatch = onlineMatch.find('table')
                    innings = onlineMatch.findAll('th')
                except:
                    input("press enter")
                    continue
                break

            i = -1
            for each in innings:
                while innings[i].text == '':
                    i -= 1
            innings = int(innings[i].text)

            while True:
                try:
                    onlineMatch = onlineMatch.findAll('tr')
                    awayTeam = onlineMatch[1].findAll('td')[2].text.strip()
                    homeTeam = onlineMatch[2].findAll('td')[2].text.strip()
                except:
                    input("press enter: ")
                    continue
                break

            if (awayTeam != 'CPU' or homeTeam != 'CPU') and innings >= 7:

                while True:
                    try:

                        summaryList = soup.find('div', {'class': 'well'}).text.strip().split()
                        summaryList = summaryList[1:3]

                        stadium = soup.findAll('div', {'class': 'section-block'})
                        stadium = stadium[3]
                    except:
                        input("Press enter: ")
                        continue
                    break
                g = []
                for br in stadium.findAll('br'):
                    next_s = br.nextSibling
                    if not (next_s and isinstance(next_s,NavigableString)):
                        continue
                    next2_s = next_s.nextSibling
                    if next2_s and isinstance(next2_s,Tag) and next2_s.name == 'br':
                        text = str(next_s).strip()
                        g.append(text)

                stadium = g[-9].split('(')[0]

                boxScore = soup.findAll('div', {'class': 'mlb20-boxscore-box'})
                if awayTeam == 'CPU':
                    myBox = boxScore[0].find('table')
                else:
                    myBox = boxScore[1].find('table')
                
                playerInfo = myBox.find('tbody')
                playerInfo = playerInfo.findAll('tr')

                pitcherAB = 0
                pitcherR = 0
                pitcherH = 0
                pitcherRBI = 0
                pitcherBB = 0
                pitcherSO = 0
                lineupPos = 1
                for each in playerInfo:
                    playerStats = each.findAll('td')
                    player = playerStats[0].text
                    position = player.split(',')[-1].strip()

                    lineupPosTemp = lineupPos
                    if player[0].isupper() == False:
                        player = player[2:]
                        lineupPos= 50
                        lineupPosTemp -= 1
                    if player.split(',')[-1] == ' P':
                        pitcherAB += int(playerStats[1].text)
                        pitcherR += int(playerStats[2].text)
                        pitcherH += int(playerStats[3].text)
                        pitcherRBI += int(playerStats[4].text)
                        pitcherBB += int(playerStats[5].text)
                        pitcherSO += int(playerStats[6].text)

                    else:
                        player = player.split(',')[0]
                        AB = playerStats[1].text
                        R = playerStats[2].text
                        H = playerStats[3].text
                        RBI = playerStats[4].text
                        BB = playerStats[5].text
                        SO = playerStats[6].text

                        if player != 'Batting Totals':
                            AVG = playerStats[7].text
                            statsFile.writerow({'Date': summaryList[0], 'Stadium': stadium, 'Lineup': lineupPos, 'Position': position, 'Player': player, 'AB': AB, 'R': R, 'H': H, 'RBI': RBI, 'BB': BB, 'SO': SO, 'AVG': AVG})
                        else:
                            AVG = float(H)/float(AB)
                            statsFile.writerow({'Date': summaryList[0], 'Stadium': stadium, 'Lineup': 100, 'Position': 'TOTALS', 'Player': player, 'AB': int(AB)-int(pitcherAB), 'R': int(R)-int(pitcherR), 'H': int(H)-int(pitcherH), 'RBI': int(RBI)-int(pitcherRBI), 'BB': int(BB)-int(pitcherBB), 'SO': int(SO)-int(pitcherSO), 'AVG': AVG})
                        lineupPos = lineupPosTemp
                        lineupPos += 1