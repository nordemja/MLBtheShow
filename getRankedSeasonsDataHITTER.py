import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import time
import json
import csv
import pandas as pd


def getHeaders():
    filename = 'headers.json'
    with open(filename) as f:
        headers = json.load(f)
    return headers

headers = getHeaders()


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