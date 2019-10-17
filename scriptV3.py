import requests
import json
import math
import datetime

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

UKCLSheet = '1fPHpp7ukvn828R0QFM-gI-C-riRvdMRyt42P32wluL4'
Div1Sheet = '16k5B3zd0Ru7Vae99uE0T768Szpo3TLfKsrSwhPDYpeo'
Div2Sheet = '1yJth-Xd6uZWzxQ8LQld6ex0NDl_eTWvBa9QSGAdaUFo'

SPREADSHEET_ID = UKCLSheet
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
    def __init__(self, nickname, kills, assists, deaths, headshots, MVPs, pentaKills, quadroKills, tripleKills, gamesPlayed, wins, roundsPlayed, roundsWon, roundsLost, points, winStreak):
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
        self.points = points
        self.winStreak = winStreak

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

offset = 0
match_IDs = []
players = []
date = datetime.datetime.now()

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 68305fc6-0fe8-4b1a-8d7d-1d1d73f8d12e',
}

UKCLHub = '2c01f318-2c99-406c-af29-6e89dc8b8aa1'
Div1Hub = 'c25f2623-2d98-4d11-9b22-bbb80dab8510'
Div2Hub = '47d463c5-692c-4357-9f19-aa2edf5ae3a9'

hub = UKCLHub

leaderboardOffset = 0

params = (
    ('offset', leaderboardOffset),
    ('limit', '1'),
)

response = requests.get('https://open.faceit.com/data/v4/leaderboards/hubs/2c01f318-2c99-406c-af29-6e89dc8b8aa1', headers=headers, params=params)
season = response.json()

if (season['items'][0]['status'] == 'UPCOMING'):
	
	leaderboardOffset = leaderboardOffset + 1
	
	params = (
		('offset', leaderboardOffset),
		('limit', '1'),
	)
	
	response = requests.get('https://open.faceit.com/data/v4/leaderboards/hubs/2c01f318-2c99-406c-af29-6e89dc8b8aa1', headers=headers, params=params)
	season = response.json()


seasonStartTime = season['items'][0]['start_date']
noMoreInSeason = False

#print(datetime.datetime.utcfromtimestamp(seasonStartTime), '\n')

print('Compiling Matches, Please Wait...')

while noMoreInSeason == False:

    params = (
        ('offset', offset + len(match_IDs)),
        ('limit', '1'),
    )

    response = requests.get('https://open.faceit.com/data/v4/hubs/' + hub + '/matches', headers=headers, params=params)
    match = response.json()
    for element in match['items']:
        if element['status'] == 'FINISHED' and element['configured_at'] > seasonStartTime:
            match_IDs.append(element['match_id'])
        elif element['status'] != 'FINISHED':
            offset = offset + 1
        elif element['configured_at'] < seasonStartTime:
            noMoreInSeason = True
            print()
            print('All matches for current Season Retreived')

    print('Matches Found: ' + str(len(match_IDs)) + ' | Cancelled Matches: ' + str(offset) + ' | Total: ' + str(len(match_IDs) + offset), end = '\r')

print(len(match_IDs), 'matches returned. A total of', len(match_IDs) + offset, 'matches were found but', offset, 'where either cancelled or did not start.')

print('Compiling Statistics, Please Wait...')
printProgressBar(0, len(match_IDs), prefix = 'Progress:', suffix = 'Complete', length = 50)

NumOfCorruptedMatches = 0

for prog, match_ID in enumerate(match_IDs):

    response = requests.get('https://open.faceit.com/data/v4/matches/' + match_ID + '/stats', headers=headers)
    matchStats = response.json()

    try:
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

                        if int(stats['Result']) == 1:
                            points = 1004
                            winStreak = 1
                        else:
                            points = 997
                            winStreak = 0

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
                                        roundsLost,
                                        points,
                                        winStreak)
                        players.append(player)
                    else:

                        if players[playerObjIndex].winStreak >= 2 and int(stats['Result']) == 1:
                            points = 6
                        elif int(stats['Result']) == 1:
                            points = 4
                        else:
                            points = -3

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
                        players[playerObjIndex].points = players[playerObjIndex].points + points

                        if int(stats['Result']) == 1:
                            players[playerObjIndex].winStreak = players[playerObjIndex].winStreak + 1
                        else:
                            players[playerObjIndex].winStreak = 0


    except KeyError:
        NumOfCorruptedMatches = NumOfCorruptedMatches + 1
    printProgressBar(prog + 1, len(match_IDs), prefix = 'Progress:', suffix = 'Complete', length = 50)

if NumOfCorruptedMatches == 0:
    print('None of the matches returned had corrupted stats.')
else:
    print(str(NumOfCorruptedMatches) + ' Matches had corrupted stats and were thus not useable.')

print('Adding to Spreadsheet, Please Wait...')

def data_sort(player):
    return player.points

players.sort(key=data_sort, reverse = True)

restructuredPlayerData = []

for index, player in enumerate(players):

    AvgKills = round_half_up((player.kills / player.gamesPlayed), 2)
    winPercent = round_half_up((player.wins / player.gamesPlayed) * 100, 2)

    if player.kills != 0 and player.headshots != 0:
        headshotPercent = round_half_up((player.headshots / player.kills) * 100, 1)
    KDRatio = round_half_up((player.kills / player.deaths), 2)
    KRRatio = round_half_up((player.kills / player.roundsPlayed), 2)
    loses = player.gamesPlayed - player.wins

    restructuredPlayerData.append([player.nickname, player.kills, player.assists, player.deaths, AvgKills, player.headshots, headshotPercent, KDRatio, KRRatio, player.MVPs, player.pentaKills, player.quadroKills, player.tripleKills, player.gamesPlayed, player.wins, loses, winPercent, player.roundsPlayed, player.roundsWon, player.roundsLost, player.points])

request = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range='A2:U1000', body={}).execute()

body = {
    'values': restructuredPlayerData
}

result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range='A5:U', valueInputOption='RAW', body=body).execute()

body = {
    'values': [['','','','','','','','Last', 'Updated', 'On', date.strftime('%d/%m/%Y'), '@', date.strftime('%I:%M %p'),'','','','','','','','',]]
}

result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range='A3:U', valueInputOption='RAW', body=body).execute()
