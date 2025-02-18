import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import json
import pandas as pd


def getHeaders():
    filename = "headers.json"
    with open(filename) as f:
        headers = json.load(f)
    return headers


headers = getHeaders()

getProfile = requests.get(
    "https://theshownation.com/mlb20/universal_profiles/CincyFan62/game_history?mode=ARENA",
    headers=headers,
)
soup = BeautifulSoup(getProfile.text, "html.parser")

totalPages = soup.find("div", {"class": "pagination"})
totalPages = totalPages.find_all("a")
totalPages = int(totalPages[3].text)
print(totalPages)


with open(
    "C:\\Users\\justi\\Documents\\Python Programming\\MLBtheShow\\rankedSeasonsStatsPITCHER.csv",
    "w",
    newline="",
    encoding="utf-8",
) as csvFile:
    statsFile = csv.DictWriter(
        csvFile,
        fieldnames=[
            "Date",
            "Stadium",
            "Player",
            "IP",
            "H",
            "R",
            "ER",
            "BB",
            "SO",
            "ERA",
        ],
    )
    statsFile.writeheader()
    for x in range(1, totalPages + 1):
        print("page: " + str(x))
        getProfile = requests.get(
            "https://theshownation.com/mlb20/universal_profiles/CincyFan62/game_history?page="
            + str(x)
            + "&mode=ARENA",
            headers=headers,
        )
        soup = BeautifulSoup(getProfile.text, "html.parser")
        getGames = soup.findAll("div", {"class": "mlb20-games-box"})
        game = 1
        for each in getGames:
            url = each.findAll("a")
            url = url[-1]
            url = "https://theshownation.com" + url["href"]
            onlineMatch = requests.get(url, headers=headers)
            soup = BeautifulSoup(onlineMatch.text, "html.parser")
            onlineMatch = soup.find("div", {"class": "section-block"})
            onlineMatch = onlineMatch.find("table")
            innings = onlineMatch.findAll("th")

            i = -1
            for each in innings:
                while innings[i].text == "":
                    i -= 1
            innings = int(innings[i].text)

            onlineMatch = onlineMatch.findAll("tr")
            awayTeam = onlineMatch[0].findAll("td")[2].text.strip()
            homeTeam = onlineMatch[2].findAll("td")[2].text.strip()

            if awayTeam != "CPU" and homeTeam != "CPU" and innings >= 7:

                Date = soup.find("div", {"class": "well"}).text.strip().split()
                Date = Date[1:3]

                stadium = soup.findAll("div", {"class": "section-block"})
                stadium = stadium[3]
                g = []
                for br in stadium.findAll("br"):
                    next_s = br.nextSibling
                    if not (next_s and isinstance(next_s, NavigableString)):
                        continue
                    next2_s = next_s.nextSibling
                    if next2_s and isinstance(next2_s, Tag) and next2_s.name == "br":
                        text = str(next_s).strip()
                        g.append(text)

                stadium = g[-9].split("(")[0]

                boxScore = soup.findAll("div", {"class": "mlb20-boxscore-box"})
                if awayTeam == "CincyFan62":
                    myBox = boxScore[0].findAll("table")[-1]
                else:
                    myBox = boxScore[1].findAll("table")[-1]

                playerInfo = myBox.find("tbody")
                playerInfo = playerInfo.findAll("tr")

                for each in playerInfo:
                    playerStats = each.findAll("td")
                    player = playerStats[0].text.split("(")[0]

                    IP = playerStats[1].text
                    H = playerStats[2].text
                    R = playerStats[3].text
                    ER = playerStats[4].text
                    BB = playerStats[5].text
                    SO = playerStats[6].text
                    try:
                        ERA = round(9 * float(ER) / float(IP), 2)
                        statsFile.writerow(
                            {
                                "Date": Date[0],
                                "Stadium": stadium,
                                "Player": player,
                                "IP": IP,
                                "H": H,
                                "R": R,
                                "ER": ER,
                                "BB": BB,
                                "SO": SO,
                                "ERA": ERA,
                            }
                        )
                    except ZeroDivisionError:
                        pass
