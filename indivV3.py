import requests
import json
import math

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

returned = 0
offset = 0
returnNum = 20
UKCL = 'UKCL'
prem = 'CS:GO 5v5 PREMIUM'
hub_Name = UKCL
stun = '664de369-fe3f-4701-9371-1e1f2c910cd2'
calc = '49c55dd0-10c8-4b56-91de-57a822fa46f9'
player_ID = calc


nickname = ''
kills = 0
assists = 0
deaths = 0
headshots = 0
MVPs = 0
pentaKills = 0
quadroKills = 0
tripleKills = 0
gamesWon = 0
roundsPlayed = 0
roundsWon = 0

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 68305fc6-0fe8-4b1a-8d7d-1d1d73f8d12e',
}

printProgressBar(0, returnNum, prefix = 'Progress:', suffix = 'Complete, Offset: ' + str(offset), length = 50)

while returned != returnNum:

    params = (
        ('game', 'csgo'),
        ('offset', offset + returned),
        ('limit', '1'),
    )

    response = requests.get('https://open.faceit.com/data/v4/players/' + player_ID + '/history', headers=headers, params=params)
    match = response.json()

    if len(match['items']) == 0:
        offset = offset + 1

    for element in match['items']:
        if element['status'] == 'finished' and element['competition_name'] == hub_Name:
            response = requests.get('https://open.faceit.com/data/v4/matches/' + element['match_id'] + '/stats', headers=headers)
            matchStats = response.json()

            try:
                for match in matchStats['rounds']:

                    matchStats = match['round_stats']
                    roundsPlayed = roundsPlayed + int(matchStats['Rounds'])

                    for team in match['teams']:

                        for player in team['players']:

                            if player['player_id'] == player_ID:

                                teamStats = team['team_stats']
                                roundsWon = roundsWon + int(teamStats['Final Score'])

                                stats = player['player_stats']

                                nickname = player['nickname']
                                kills = kills + int(stats['Kills'])
                                assists = assists + int(stats['Assists'])
                                deaths = deaths + int(stats['Deaths'])
                                headshots = headshots + int(stats['Headshot'])
                                MVPs = MVPs + int(stats['MVPs'])
                                pentaKills = pentaKills + int(stats['Penta Kills'])
                                quadroKills = quadroKills + int(stats['Quadro Kills'])
                                tripleKills = tripleKills + int(stats['Triple Kills'])
                                gamesWon = gamesWon + int(stats['Result'])
                    returned = returned + 1


            except KeyError:
                offset = offset + 1


        else:
            offset = offset + 1
    printProgressBar(returned, returnNum, prefix = 'Progress:', suffix = 'Complete, Offset: ' + str(offset), length = 50)

print('Stats for', nickname, 'in the last', returnNum, 'games of', hub_Name, ':')
print('Kills:', kills)
print('Assists:', assists)
print('Deaths:', deaths)
print('Avg Kills:', round_half_up(kills / returned, 2))
print('Headshots:', headshots)
print('Headshot %:', round_half_up((headshots / kills) * 100, 1))
print('K/D Ratio:', round_half_up((kills / deaths), 2))
print('K/R Ratio:', round_half_up((kills / roundsPlayed), 2))
print('MVPs:', MVPs)
print('Penta Kills:', pentaKills)
print('Quadro Kills', quadroKills)
print('Triple Kills', tripleKills)
print('Games Won:', gamesWon)
print('Games Lost:', returned - gamesWon)
print('Rounds Played:', roundsPlayed)
print('Rounds Won:', roundsWon)
print('Rounds Lost:', roundsPlayed - roundsWon)
