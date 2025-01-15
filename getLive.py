from flask import Flask, jsonify
from flask_cors import CORS
from nba_api.live.nba.endpoints import scoreboard, boxscore
import math

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"])  # Allow only requests from Node.js server

@app.route('/live_scores', methods=['GET'])
    
def get_live_scores():
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()

    updates = []
    for game in games:
        updates.append({
            "time": game['gameStatusText'],
            "homeTeam": game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName'],
            "homeScore": game['homeTeam']['score'],
            "awayTeam": game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'],
            "awayScore": game['awayTeam']['score'],
            "period": game['period'],
            "rem": game['gameClock']
        })

    return jsonify(updates)

# Determine which game is the most exciting

def excitement_score(game):
    home_score = game['homeTeam']['score']
    away_score = game['awayTeam']['score']
    rem = time_remaining(game)
    period = game['period']

    score_differential = abs(home_score - away_score)
    q4_bonus = 1 if period == 4 else 0
    overtime_bonus = 1 if period > 4 else 0

    w1, w2, w3, w4 = 0.5, 50, 1, 1.25

    excitement_score = (
        w1 * (1 / max(score_differential, 1)) +     # Closer scores are better
        w2 * (1 / max(rem, 1)) +                    # Less time remaining is better
        w3 * q4_bonus +                             # Boost for 4th quarter
        w4 * overtime_bonus                         # Boost for overtime
    )

    return excitement_score

def most_exciting():
    board = scoreboard.ScoreBoard()
    #games = board.games.get_dict()
    games = [
    {
        'gameId': '009',
        'gameStatus': 2,
        'gameStatusText': 'Q2 7:30',
        'period': 2,
        'gameClock': '7:30',
        'homeTeam': {'teamCity': 'Nets', 'teamName': 'Brooklyn', 'score': 49},
        'awayTeam': {'teamCity': 'Pacers', 'teamName': 'Indiana', 'score': 45},
    },
    {
        'gameId': '010',
        'gameStatus': 2,
        'gameStatusText': 'Q4 4:50',
        'period': 4,
        'gameClock': '4:50',
        'homeTeam': {'teamCity': 'Bucks', 'teamName': 'Milwaukee', 'score': 95},
        'awayTeam': {'teamCity': 'Raptors', 'teamName': 'Toronto', 'score': 96},
    },
    {
        'gameId': '011',
        'gameStatus': 2,
        'gameStatusText': 'Q3 6:00',
        'period': 3,
        'gameClock': '6:00',
        'homeTeam': {'teamCity': 'Hornets', 'teamName': 'Charlotte', 'score': 72},
        'awayTeam': {'teamCity': 'Magic', 'teamName': 'Orlando', 'score': 70},
    },
    {
        'gameId': '012',
        'gameStatus': 2,
        'gameStatusText': 'Q1 4:20',
        'period': 1,
        'gameClock': '4:20',
        'homeTeam': {'teamCity': 'Jazz', 'teamName': 'Utah', 'score': 28},
        'awayTeam': {'teamCity': 'Trail Blazers', 'teamName': 'Portland', 'score': 30},
    },
    {
        'gameId': '013',
        'gameStatus': 2,
        'gameStatusText': 'Q5 2:30',
        'period': 5,
        'gameClock': '2:30',
        'homeTeam': {'teamCity': 'Grizzlies', 'teamName': 'Memphis', 'score': 116},
        'awayTeam': {'teamCity': 'Timberwolves', 'teamName': 'Minnesota', 'score': 118},
    },
    {
        'gameId': '014',
        'gameStatus': 2,
        'gameStatusText': 'Q4 1:10',
        'period': 4,
        'gameClock': '1:10',
        'homeTeam': {'teamCity': 'Cavaliers', 'teamName': 'Cleveland', 'score': 101},
        'awayTeam': {'teamCity': 'Pistons', 'teamName': 'Detroit', 'score': 104},
    },
    {
        'gameId': '015',
        'gameStatus': 2,
        'gameStatusText': 'Q2 10:00',
        'period': 2,
        'gameClock': '10:00',
        'homeTeam': {'teamCity': 'Kings', 'teamName': 'Sacramento', 'score': 40},
        'awayTeam': {'teamCity': 'Wizards', 'teamName': 'Washington', 'score': 38},
    },
    {
        'gameId': '016',
        'gameStatus': 2,
        'gameStatusText': 'Q4 0:30',
        'period': 4,
        'gameClock': '0:30',
        'homeTeam': {'teamCity': 'Pelicans', 'teamName': 'New Orleans', 'score': 109},
        'awayTeam': {'teamCity': 'Spurs', 'teamName': 'San Antonio', 'score': 108},
    },
    {
        'gameId': '017',
        'gameStatus': 2,
        'gameStatusText': 'Q3 9:15',
        'period': 3,
        'gameClock': '9:15',
        'homeTeam': {'teamCity': 'Rockets', 'teamName': 'Houston', 'score': 62},
        'awayTeam': {'teamCity': 'Warriors', 'teamName': 'Golden State', 'score': 71},
    },
    {
        'gameId': '018',
        'gameStatus': 2,
        'gameStatusText': 'Q1 11:45',
        'period': 1,
        'gameClock': '11:45',
        'homeTeam': {'teamCity': 'Thunder', 'teamName': 'Oklahoma City', 'score': 2},
        'awayTeam': {'teamCity': 'Mavericks', 'teamName': 'Dallas', 'score': 0},
    },
]



    # x = boxscore.BoxScore(game_id='0022400501')
    # game_data = x.get_dict()

    # print(game_data)

    # if 

    games_list = []
    for game in games:
        if game['gameStatus'] == 2:
            game_score = excitement_score(game)
            games_list.append((game, game_score))

    games_list.sort(key=lambda x: x[1], reverse=True)

    for game, score in games_list:
        home = game['homeTeam']
        away = game['awayTeam']
        print(f"{home['teamCity']} {home['score']}, {away['teamCity']} {away['score']} -- Time Remaining: Q{game['period']} {game['gameClock']} -- Excitement Factor: {score:.4f}")
        print(f"http://topstreams.info/nba/{game['homeTeam']['teamName']}")

# Return time remaining in seconds
def time_remaining(game):
    try:
        minutes, seconds = map(int, game['gameClock'].split(":"))
    except ValueError: # api glitches sometimes -- e.g. PT07M28.00S
        print(f"Invalid clock data")
        return -1
    
    match game['period']:
        case 1:
            total_minutes = minutes + 36
        case 2:
            total_minutes = minutes + 24
        case 3:
            total_minutes = minutes + 12
        case _:                             # 4th quarter or overtime
            total_minutes = minutes
        
    total_seconds = (total_minutes * 60) + seconds
    
    return total_seconds


if __name__ == "__main__":
    # app.run(port=5000)
    most_exciting()

# {'gameId': '0022400560', 'gameCode': '20250114/BKNPOR', 'gameStatus': 2, 'gameStatusText': '4th Qtr             ', 'period': 4, 'gameClock': '3:13 ', 'gameTimeUTC': '2025-01-15T03:00:00Z', 'gameEt': '2025-01-14T22:00:00Z', 'regulationPeriods': 4, 'ifNecessary': False, 'seriesGameNumber': '', 'gameLabel': '', 'gameSubLabel': '', 'seriesText': '', 'seriesConference': '', 'poRoundDesc': '', 'gameSubtype': '', 'homeTeam': {'teamId': 1610612757, 'teamName': 'Trail Blazers', 'teamCity': 'Portland', 'teamTricode': 'POR', 'wins': 13, 'losses': 25, 'score': 108, 'seed': None, 'inBonus': None, 'timeoutsRemaining': 2, 'periods': [{'period': 1, 'periodType': 'REGULAR', 'score': 30}, {'period': 2, 'periodType': 'REGULAR', 'score': 31}, {'period': 3, 'periodType': 'REGULAR', 'score': 27}, {'period': 4, 'periodType': 'REGULAR', 'score': 20}]}, 'awayTeam': {'teamId': 1610612751, 'teamName': 'Nets', 'teamCity': 'Brooklyn', 'teamTricode': 'BKN', 'wins': 13, 'losses': 26, 'score': 121, 'seed': None, 'inBonus': None, 'timeoutsRemaining': 1, 'periods': [{'period': 1, 'periodType': 'REGULAR', 'score': 40}, {'period': 2, 'periodType': 'REGULAR', 'score': 26}, {'period': 3, 'periodType': 'REGULAR', 'score': 32}, {'period': 4, 'periodType': 'REGULAR', 'score': 23}]}, 'gameLeaders': {'homeLeaders': {'personId': 1630703, 'name': 'Scoot Henderson', 'jerseyNum': '00', 'position': 'G', 'teamTricode': 'POR', 'playerSlug': None, 'points': 36, 'rebounds': 4, 'assists': 6}, 'awayLeaders': {'personId': 1629661, 'name': 'Cameron Johnson', 'jerseyNum': '2', 'position': 'F', 'teamTricode': 'BKN', 'playerSlug': None, 'points': 24, 'rebounds': 1, 'assists': 2}}, 'pbOdds': {'team': None, 'odds': 0.0, 'suspended': 0}}