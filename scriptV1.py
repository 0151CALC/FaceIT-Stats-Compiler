import requests
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('My Project-877612993710.json')) # json credentials you downloaded earlier
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

file = gspread.authorize(credentials)

#sheet = file.open("UKCL Stats").sheet1

class Player:
    def __init__(self, nickname, kills, assists, deaths, headshots, headshotPercentage, KD, KR, MVPs, pentaKills, quadroKills, tripleKills, gamesPlayed, wins, loses):
        self.nickname = nickname
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
        self.headshots = headshots
        self.headshotPercentage = headshotPercentage
        self.KD = KD
        self.KR = KR
        self.MVPs = MVPs
        self.pentaKills = pentaKills
        self.quadroKills = quadroKills
        self.tripleKills = tripleKills
        self.gamesPlayed = gamesPlayed
        self.wins = wins
        self.loses = loses

returnNum = 50;
returnNumString = str(returnNum * 3)

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 68305fc6-0fe8-4b1a-8d7d-1d1d73f8d12e',
}

params = (
    ('type', 'past'),
    ('limit', returnNumString),
)

response = requests.get('https://open.faceit.com/data/v4/hubs/2c01f318-2c99-406c-af29-6e89dc8b8aa1/matches', headers=headers, params=params)
data = response.json()

match_IDs = []
players = []

for element in data['items']:

    if element['status'] != 'CANCELLED':
        match_IDs.append(element['match_id'])

    if len(match_IDs) == returnNum:
        break

print(match_IDs)

for match_ID in match_IDs:
    print('https://open.faceit.com/data/v4/matches/' + match_ID + '/stats')

    response = requests.get('https://open.faceit.com/data/v4/matches/' + match_ID + '/stats', headers=headers, params=params)
    matchStats = response.json()

    for match in matchStats['rounds']:
        for team in match['teams']:
            for player in team['players']:

                playerName = player['nickname']

                stats = player['player_stats']

                playerExists = False
                playerObjIndex = -1

                for index, obj in enumerate(players):

                    if obj.nickname == playerName:
                        print('Already Contained')
                        playerObjIndex = index
                        playerExists = True
                        break

                if stats['Result'] == 1:
                    loss = 0
                else:
                    loss = 1

                if playerExists == False:

                    player = Player(playerName,
                                    int(stats['Kills']),
                                    int(stats['Assists']),
                                    int(stats['Deaths']),
                                    int(stats['Headshot']),
                                    int(stats['Headshots %']),
                                    float(stats['K/D Ratio']),
                                    float(stats['K/R Ratio']),
                                    int(stats['MVPs']),
                                    int(stats['Penta Kills']),
                                    int(stats['Quadro Kills']),
                                    int(stats['Triple Kills']),
                                    1,
                                    int(stats['Result']),
                                    loss)
                    players.append(player)

                else:

                    print(playerObjIndex)

                    players[playerObjIndex].kills = players[playerObjIndex].kills + int(stats['Kills'])
                    players[playerObjIndex].assists = players[playerObjIndex].assists + int(stats['Assists'])
                    players[playerObjIndex].deaths = players[playerObjIndex].deaths + int(stats['Deaths'])
                    players[playerObjIndex].headshots = players[playerObjIndex].headshots + int(stats['Headshot'])
                    players[playerObjIndex].MVPs = players[playerObjIndex].MVPs + int(stats['MVPs'])
                    players[playerObjIndex].pentaKills = players[playerObjIndex].pentaKills + int(stats['Penta Kills'])
                    players[playerObjIndex].quadroKills = players[playerObjIndex].quadroKills + int(stats['Quadro Kills'])
                    players[playerObjIndex].tripleKills = players[playerObjIndex].tripleKills + int(stats['Triple Kills'])
                    players[playerObjIndex].gamesPlayed = players[playerObjIndex].gamesPlayed + 1
                    players[playerObjIndex].wins = players[playerObjIndex].wins + int(stats['Result'])
                    players[playerObjIndex].loses = players[playerObjIndex].loses + loss



print(": Nickname       : Kills : Assists : Deaths : Headshots : MVPs : Penta Kills : Quadro Kills : Triple Kills : Games Played : Total Wins : Total Loses :")

for player in players:

    print(":", player.nickname, " "*(13-len(player.nickname)), ":",
               player.kills, " "*(4-len(str(player.kills))), ":",
               player.assists, " "*(6-len(str(player.assists))), ":",
               player.deaths, " "*(5-len(str(player.deaths))), ":",
               player.headshots, " "*(8-len(str(player.headshots))), ":",
               player.MVPs, " "*(3-len(str(player.MVPs))), ":",
               player.pentaKills, " "*(10-len(str(player.pentaKills))), ":",
               player.quadroKills, " "*(11-len(str(player.quadroKills))), ":",
               player.tripleKills, " "*(11-len(str(player.tripleKills))), ":",
               player.gamesPlayed, " "*(11-len(str(player.gamesPlayed))), ":",
               player.wins, " "*(9-len(str(player.wins))), ":",
               player.loses, " "*(10-len(str(player.loses))), ":",
        )

#sheet.update_cell(1, 1, "this works! :)")
