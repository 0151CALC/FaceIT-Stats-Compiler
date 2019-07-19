import requests
import json
import math

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

UKCLSheet = '1fPHpp7ukvn828R0QFM-gI-C-riRvdMRyt42P32wluL4'
Div1Sheet = '16k5B3zd0Ru7Vae99uE0T768Szpo3TLfKsrSwhPDYpeo'
Div2Sheet = '1yJth-Xd6uZWzxQ8LQld6ex0NDl_eTWvBa9QSGAdaUFo'

SPREADSHEET_ID = Div2Sheet
SAMPLE_RANGE_NAME = 'Sheet1!A2:N'

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'C:/Users/Callum/OneDrive/Programming/Python/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

class Player:
    def __init__(self, nickname, kills, assists, deaths, headshots, MVPs, pentaKills, quadroKills, tripleKills, gamesPlayed, wins, roundsPlayed, roundsWon, roundsLost):
        self.nickname = nickname
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
        self.headshots = headshots
        self.MVPs = MVPs
        self.pentaKills = pentaKills
        self.quadroKills = quadroKills
        self.tripleKills = tripleKills
        self.gamesPlayed = gamesPlayed
        self.wins = wins
        self.roundsPlayed = roundsPlayed
        self.roundsWon = roundsWon
        self.roundsLost = roundsLost

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total:
        print()

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

returnNum = 100
offset = 0
match_IDs = []
players = []

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 68305fc6-0fe8-4b1a-8d7d-1d1d73f8d12e',
}
print('Compiling Matches, Please Wait...')
printProgressBar(0, returnNum, prefix = 'Progress:', suffix = 'Complete', length = 50)

UKCLHub = '2c01f318-2c99-406c-af29-6e89dc8b8aa1'
Div1Hub = 'c25f2623-2d98-4d11-9b22-bbb80dab8510'
Div2Hub = '47d463c5-692c-4357-9f19-aa2edf5ae3a9'

hub = Div2Hub

while len(match_IDs) != returnNum:

    params = (
        ('offset', offset + len(match_IDs)),
        ('limit', '1'),
    )

    response = requests.get('https://open.faceit.com/data/v4/hubs/' + hub + '/matches', headers=headers, params=params)
    match = response.json()
    for element in match['items']:

        if element['status'] == 'FINISHED':
            match_IDs.append(element['match_id'])
            printProgressBar(len(match_IDs), returnNum, prefix = 'Progress:', suffix = 'Complete', length = 50)
        else:
            offset = offset + 1

print(len(match_IDs), 'matches returned. A total of', len(match_IDs) + offset, 'matches were found but', offset, 'where either cancelled or did not start.')

print('Compiling Statistics, Please Wait...')
printProgressBar(0, returnNum, prefix = 'Progress:', suffix = 'Complete', length = 50)

for prog, match_ID in enumerate(match_IDs):

    response = requests.get('https://open.faceit.com/data/v4/matches/' + match_ID + '/stats', headers=headers)
    matchStats = response.json()

    for match in matchStats['rounds']:

        matchStats = match['round_stats']
        numRounds = int(matchStats['Rounds'])

        for team in match['teams']:

            teamStats = team['team_stats']
            roundsWon = int(teamStats['Final Score'])
            roundsLost = numRounds - roundsWon

            for player in team['players']:

                playerName = player['nickname']
                stats = player['player_stats']
                playerExists = False
                playerObjIndex = -1

                for index, player in enumerate(players):
                    if player.nickname == playerName:
                        playerObjIndex = index
                        playerExists = True
                        break

                if playerExists == False:

                    player = Player(playerName,
                                    int(stats['Kills']),
                                    int(stats['Assists']),
                                    int(stats['Deaths']),
                                    int(stats['Headshot']),
                                    int(stats['MVPs']),
                                    int(stats['Penta Kills']),
                                    int(stats['Quadro Kills']),
                                    int(stats['Triple Kills']),
                                    1,
                                    int(stats['Result']),
                                    numRounds,
                                    roundsWon,
                                    roundsLost)
                    players.append(player)
                else:

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
                    players[playerObjIndex].roundsPlayed = players[playerObjIndex].roundsPlayed + numRounds
                    players[playerObjIndex].roundsWon = players[playerObjIndex].roundsWon + roundsWon
                    players[playerObjIndex].roundsLost = players[playerObjIndex].roundsLost + roundsLost
    printProgressBar(prog, returnNum, prefix = 'Progress:', suffix = 'Complete', length = 50)
#print(": Nickname       : Kills : Assists : Deaths : Headshots : Headshot % : K/D Ratio : K/R Ratio : MVPs : Penta Kills : Quadro Kills : Triple Kills : Games Played : Total Wins : Total Loses : Rounds Played : Rounds Won : Rounds Lost :")

print('Adding to Spreadsheet, Please Wait...')

restructuredPlayerData = []

for index, player in enumerate(players):

    headshotPercent = round_half_up((player.headshots / player.kills) * 100, 1)
    KDRatio = round_half_up((player.kills / player.deaths), 2)
    KRRatio = round_half_up((player.kills / player.roundsPlayed), 2)
    loses = player.gamesPlayed - player.wins

    #print(":", player.nickname, " "*(13-len(player.nickname)), ":",
    #           player.kills, " "*(4-len(str(player.kills))), ":",
    #           player.assists, " "*(6-len(str(player.assists))), ":",
    #           player.deaths, " "*(5-len(str(player.deaths))), ":",
    #           player.headshots, " "*(8-len(str(player.headshots))), ":",
    #           headshotPercent, " "*(9-len(str(headshotPercent))), ":",
    #           KDRatio, " "*(6-len(str(KDRatio))), ":",
    #           KRRatio, " "*(6-len(str(KRRatio))), ":",
    #           player.MVPs, " "*(3-len(str(player.MVPs))), ":",
    #           player.pentaKills, " "*(10-len(str(player.pentaKills))), ":",
    #           player.quadroKills, " "*(11-len(str(player.quadroKills))), ":",
    #           player.tripleKills, " "*(11-len(str(player.tripleKills))), ":",
    #           player.gamesPlayed, " "*(11-len(str(player.gamesPlayed))), ":",
    #           player.wins, " "*(9-len(str(player.wins))), ":",
    #           player.loses, " "*(10-len(str(player.loses))), ":",
    #           player.roundsPlayed, " "*(12-len(str(player.roundsPlayed))), ":",
    #           player.roundsWon, " "*(9-len(str(player.roundsWon))), ":",
    #           player.roundsLost, " "*(10-len(str(player.roundsLost))), ":",
    #)

    restructuredPlayerData.append([player.nickname, player.kills, player.assists, player.deaths, player.headshots, headshotPercent, KDRatio, KRRatio, player.MVPs, player.pentaKills, player.quadroKills, player.tripleKills, player.gamesPlayed, player.wins, loses, player.roundsPlayed, player.roundsWon, player.roundsLost])


body = {
    'values': restructuredPlayerData
}

result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range='A2:R', valueInputOption='RAW', body=body).execute()
