import requests
import json
import sqlite3
import time

# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

API_KEY = "RGAPI-7ef8a15d-cdbb-4382-b12b-283d10f1ede4"

regions = {"euw1": "https://www.leagueofgraphs.com/pl/rankings/summoners/euw/page-",
           "na1": "https://www.leagueofgraphs.com/pl/rankings/summoners/na/page-",
           "kr": "https://www.leagueofgraphs.com/pl/rankings/summoners/kr/page-",
           "br1": "https://www.leagueofgraphs.com/pl/rankings/summoners/br/page-",
           "eun1": "https://www.leagueofgraphs.com/pl/rankings/summoners/eune/page-",
           "jp1": "https://www.leagueofgraphs.com/pl/rankings/summoners/jp/page-",
           "la1": "https://www.leagueofgraphs.com/pl/rankings/summoners/lan/page-",
           "la2": "https://www.leagueofgraphs.com/pl/rankings/summoners/las/page-",
           "ru": "https://www.leagueofgraphs.com/pl/rankings/summoners/ru/page-",
           "tr1": "https://www.leagueofgraphs.com/pl/rankings/summoners/tr/page-"
           }


def check_game_version(game_version):
    return game_version[0:5] == "10.25"


def get_player_id(region, player_name):
    x = requests.get(
        "https://%s.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s?api_key=%s" % (
            region, player_name, API_KEY)).content
    json_data = json.loads(x)

    try:
        return json_data['accountId']
    except KeyError:
        print("NAME_ERROR")
        return "NAME_ERROR"


def get_players_match_list(region, player_id):
    second_link = "https://%s.api.riotgames.com/lol/match/v4/matchlists/by-account/%s?queue=420&api_key=%s" % (
        region, player_id, API_KEY)
    x = requests.get(second_link).content
    json_data = json.loads(x)

    try:
        return [v['gameId'] for v in json_data['matches']]
    except KeyError:
        print("KeyError - get_players_match_list")
        return []


def get_match(region, match_id):
    link = 'https://%s.api.riotgames.com/lol/match/v4/matches/%s?api_key=%s' % (
        region, match_id, API_KEY)
    game = json.loads(requests.get(link).content)
    try:
        if check_game_version(game['gameVersion']):
            game_id = match_id
            platform = game['platformId']
            game_duration = game['gameDuration']
            team = game['teams'][0]
            # Start from blue side perspective
            winner = team['win']
            first_blood = team["firstBlood"]
            first_tower = team["firstTower"]
            first_dragon = team["firstDragon"]
            first_rift_herald = team["firstRiftHerald"]

            participants = []
            for participant in game['participants']:
                participants.append(participant['championId'])
                participants.append(participant['timeline']['role'])
                participants.append(participant['timeline']['lane'])

            return (game_id, platform, game_duration, winner, first_blood, first_tower, first_dragon,
                    first_rift_herald) + tuple(
                participants)
        print("bg")
        return "bg"
    except KeyError:
        print("KeyError - get_match")
        return "bg"


def insert_match_to_db(match):
    conn = sqlite3.connect('lol.db')
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO GAMES
                        VALUES (?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?)
                        """, match)

    conn.commit()
    conn.close()


def job_in_region(region, index):
    conn = sqlite3.connect('lol.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM PLAYERS WHERE Region = ?""", (region,))
    players = cursor.fetchall()

    player = players[index]

    conn.commit()
    conn.close()

    player_id = get_player_id(region, player[0])

    matches_id = []
    if player_id != "NAME_ERROR" and player_id != "":
        matches_id += get_players_match_list(region, player_id)
    else:
        return

    bg_counter = 0
    for index, match_id in enumerate(matches_id):
        if index < 95:
            if index % 15 == 1:
                time.sleep(1)
            current_match = get_match(region, match_id)
            if current_match != 'bg':
                insert_match_to_db(current_match)
            else:
                bg_counter += 1
                if bg_counter > 0:
                    return


for i in range(4000, 5000):
    print('current index: ' + str(i))
    for r in regions.keys():
        job_in_region(r, i)


