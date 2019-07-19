import requests
import json

nickname = "Lewis"
kills = 0
assists = 0
deaths = 0
headshots = 0
headshotPercentage = 0
KD = 0
KR = 0
MVPs = 0
pentaKills = 0
quadroKills = 0
tripleKills = 0
gamesPlayed = 0
wins = 0
loses = 0

returnNum = 100;
returnNumString = str(returnNum * 10)

print(returnNumString)

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 68305fc6-0fe8-4b1a-8d7d-1d1d73f8d12e',
}

params = (
    ('game', 'csgo'),
    ('offset', '0'),
    ('limit', returnNumString),
)

response = requests.get('https://open.faceit.com/data/v4/players/59468f0a-b337-4cdf-afaa-29020d2473c1/history', headers=headers, params=params)
data = response.json()

print(len(data['items']))

match_IDs = []
players = []

for element in data['items']:

    if element['status'] == "finished" and element['competition_name'] == "UKCL":
        match_IDs.append(element['match_id'])

    if len(match_IDs) == returnNum * 2:
        break

print(match_IDs)
print(len(match_IDs))

for match_ID in match_IDs:
    print('https://open.faceit.com/data/v4/matches/' + match_ID + '/stats')

    response = requests.get('https://open.faceit.com/data/v4/matches/' + match_ID + '/stats', headers=headers, params=params)
    matchStats = response.json()

    for match in matchStats['rounds']:
        for team in match['teams']:
            for player in team['players']:

                stats = player['player_stats']

                if int(stats['Result']) == 1:
                    loss = 0
                else:
                    loss = 1

                if player['nickname'] == nickname:
                    kills = kills + int(stats['Kills'])
                    assists = assists + int(stats['Assists'])
                    deaths = deaths + int(stats['Deaths'])
                    headshots = headshots + int(stats['Headshot'])
                    MVPs = MVPs + int(stats['MVPs'])
                    pentaKills = pentaKills + int(stats['Penta Kills'])
                    quadroKills = quadroKills + int(stats['Quadro Kills'])
                    tripleKills = tripleKills + int(stats['Triple Kills'])
                    gamesPlayed = gamesPlayed + 1
                    wins = wins + int(stats['Result'])
                    loses = loses + loss

                if gamesPlayed == returnNum:
                    break;

print(": Nickname       : Kills : Assists : Deaths : Headshots : MVPs : Penta Kills : Quadro Kills : Triple Kills : Games Played : Total Wins : Total Loses :")
print(":", nickname, " "*(13-len(nickname)), ":",
           kills, " "*(4-len(str(kills))), ":",
           assists, " "*(6-len(str(assists))), ":",
           deaths, " "*(5-len(str(deaths))), ":",
           headshots, " "*(8-len(str(headshots))), ":",
           MVPs, " "*(3-len(str(MVPs))), ":",
           pentaKills, " "*(10-len(str(pentaKills))), ":",
           quadroKills, " "*(11-len(str(quadroKills))), ":",
           tripleKills, " "*(11-len(str(tripleKills))), ":",
           gamesPlayed, " "*(11-len(str(gamesPlayed))), ":",
           wins, " "*(9-len(str(wins))), ":",
           loses, " "*(10-len(str(loses))), ":",
    )
