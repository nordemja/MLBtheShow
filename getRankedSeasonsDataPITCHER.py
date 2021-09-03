import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import pandas as pd


headers = {
    'authority': 'theshownation.com',
    'accept': 'text/html, application/xhtml+xml',
    'turbolinks-referrer': 'https://theshownation.com/mlb20/community_market?display_position=&amp;max_best_buy_price=&amp;max_best_sell_price=&amp;max_rank=84&amp;min_best_buy_price=1000&amp;min_best_sell_price=&amp;min_rank=&amp;name=&amp;player_type_id=&amp;rarity_id=&amp;series_id=1337&amp;team_id=&amp;type=mlb_card',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://theshownation.com/mlb20/community_market?display_position=&amp;max_best_buy_price=&amp;max_best_sell_price=&amp;max_rank=84&amp;min_best_buy_price=1000&amp;min_best_sell_price=&amp;min_rank=&amp;name=&amp;player_type_id=&amp;rarity_id=&amp;series_id=1337&amp;team_id=&amp;type=mlb_card',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ga=GA1.2.1852743341.1605549956; _gid=GA1.2.816802570.1605549956; tsn_last_seen_roster_id=18; tsn_token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NDQ1MDgsInVzZXJuYW1lIjoiQ2luY3lGYW42MiIsInBpY3R1cmUiOiJodHRwczovL3N0YXRpYy1yZXNvdXJjZS5ucC5jb21tdW5pdHkucGxheXN0YXRpb24ubmV0L2F2YXRhci9XV1NfRS9FMDAyMC5wbmciLCJncm91cHMiOltdfQ.xPGBL5SKPRuBrAeQbjgbfqXxzEaispOVyLho_tgX4Ys; _tsn_session=79508495d49073c80ed86f4144eefd84',
    'if-none-match': 'W/"6847f72878fbc7047fa7a11858af5c98"',
}

getProfile = requests.get('https://theshownation.com/mlb20/universal_profiles/CincyFan62/game_history?mode=ARENA', headers=headers)
soup = BeautifulSoup(getProfile.text, 'html.parser')

totalPages = soup.find('div', {'class': 'pagination'})
totalPages = totalPages.find_all('a')
totalPages =  int(totalPages[3].text)
print(totalPages)


with open('C:\\Users\\justi\\Documents\\Python Programming\\MLBtheShow\\rankedSeasonsStatsPITCHER.csv', 'w', newline='', encoding='utf-8') as csvFile:
    statsFile = csv.DictWriter(csvFile, fieldnames=['Date', 'Stadium', 'Player', 'IP', 'H', 'R', 'ER', 'BB', 'SO', 'ERA'])
    statsFile.writeheader()
    for x in range(1, totalPages+1):
        print("page: " +str(x))
        getProfile = requests.get('https://theshownation.com/mlb20/universal_profiles/CincyFan62/game_history?page='+str(x)+'&mode=ARENA', headers=headers)
        soup = BeautifulSoup(getProfile.text, 'html.parser')
        getGames = soup.findAll('div', {'class': 'mlb20-games-box'})
        game = 1
        for each in getGames:
            url = each.findAll('a')
            url = url[-1]
            url =  'https://theshownation.com' + url['href']
            onlineMatch = requests.get(url, headers=headers)
            soup = BeautifulSoup(onlineMatch.text, 'html.parser')
            onlineMatch = soup.find('div', {'class': 'section-block'})
            onlineMatch = onlineMatch.find('table')
            innings = onlineMatch.findAll('th')

            i = -1
            for each in innings:
                while innings[i].text == '':
                    i -= 1
            innings = int(innings[i].text)

            onlineMatch = onlineMatch.findAll('tr')
            awayTeam = onlineMatch[0].findAll('td')[2].text.strip()
            homeTeam = onlineMatch[2].findAll('td')[2].text.strip()

            if awayTeam != 'CPU' and homeTeam != 'CPU' and innings >= 7:

                Date = soup.find('div', {'class': 'well'}).text.strip().split()
                Date = Date[1:3]

                stadium = soup.findAll('div', {'class': 'section-block'})
                stadium = stadium[3]
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
                if awayTeam == 'CincyFan62':
                    myBox = boxScore[0].findAll('table')[-1]
                else:
                    myBox = boxScore[1].findAll('table')[-1]
                
                playerInfo = myBox.find('tbody')
                playerInfo = playerInfo.findAll('tr')

                for each in playerInfo:
                    playerStats = each.findAll('td')
                    player = playerStats[0].text.split('(')[0]

                    IP = playerStats[1].text
                    H = playerStats[2].text
                    R = playerStats[3].text
                    ER = playerStats[4].text
                    BB = playerStats[5].text
                    SO = playerStats[6].text
                    try:
                        ERA = round(9 * float(ER)/float(IP),2)
                        statsFile.writerow({'Date': Date[0], 'Stadium': stadium, 'Player': player, 'IP': IP, 'H': H, 'R': R, 'ER': ER, 'BB': BB, 'SO': SO, 'ERA': ERA})
                    except ZeroDivisionError:
                        pass
