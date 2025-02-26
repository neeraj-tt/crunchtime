from flask import Flask, jsonify
from flask_cors import CORS
from nba_api.live.nba.endpoints import scoreboard
import re

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"]) # Allow only requests from Node.js server

'''games = [
    {
        'gameId': '025',
        'gameStatus': 2,
        'gameStatusText': 'Q4 5:30',
        'period': 4,
        'gameClock': '5:30',
        'homeTeam': {'teamCity': 'Toronto', 'teamName': 'Raptors', 'score': 102},
        'awayTeam': {'teamCity': 'Houston', 'teamName': 'Rockets', 'score': 88},
    },
    {
        'gameId': '026',
        'gameStatus': 2,
        'gameStatusText': 'Q3 9:45',
        'period': 3,
        'gameClock': '9:45',
        'homeTeam': {'teamCity': 'Orlando', 'teamName': 'Magic', 'score': 58},
        'awayTeam': {'teamCity': 'Golden State', 'teamName': 'Warriors', 'score': 74},
    },
    {
        'gameId': '027',
        'gameStatus': 2,
        'gameStatusText': 'Q4 1:20',
        'period': 4,
        'gameClock': '1:20',
        'homeTeam': {'teamCity': 'San Antonio', 'teamName': 'Spurs', 'score': 91},
        'awayTeam': {'teamCity': 'Los Angeles', 'teamName': 'Clippers', 'score': 93},
    },
    {
        'gameId': '028',
        'gameStatus': 2,
        'gameStatusText': 'Q2 4:50',
        'period': 2,
        'gameClock': '4:50',
        'homeTeam': {'teamCity': 'Indiana', 'teamName': 'Pacers', 'score': 45},
        'awayTeam': {'teamCity': 'Chicago', 'teamName': 'Bulls', 'score': 47},
    },
    {
        'gameId': '029',
        'gameStatus': 2,
        'gameStatusText': 'Q5 3:10',
        'period': 5,
        'gameClock': '3:10',
        'homeTeam': {'teamCity': 'Utah', 'teamName': 'Jazz', 'score': 116},
        'awayTeam': {'teamCity': 'Memphis', 'teamName': 'Grizzlies', 'score': 118},
    },
    {
        'gameId': '030',
        'gameStatus': 2,
        'gameStatusText': 'Q1 8:15',
        'period': 1,
        'gameClock': '8:15',
        'homeTeam': {'teamCity': 'Detroit', 'teamName': 'Pistons', 'score': 10},
        'awayTeam': {'teamCity': 'Cleveland', 'teamName': 'Cavaliers', 'score': 18},
    },
]'''

@app.route('/live_scores', methods=['GET'])    
def get_live_scores():
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()

    updates = []
    for game in games:
        updates.append({
            "time": game['gameStatusText'],
            "homeCity": game['homeTeam']['teamCity'],
            "homeTeam": game['homeTeam']['teamName'],
            "homeTricode": game['homeTeam']['teamTricode'],
            "homeScore": game['homeTeam']['score'],
            "awayCity": game['awayTeam']['teamCity'],
            "awayTeam": game['awayTeam']['teamName'],
            "awayTricode": game['awayTeam']['teamTricode'],
            "awayScore": game['awayTeam']['score'],
            "period": game['period'],
            "rem": game['gameClock'],
            "exciting": excitement_score(game)
        })
        
    response = {
        "updates": updates,
        "mostExciting": most_exciting()
    }

    return jsonify(response)

# Give each game a "score" in terms of how exciting it is
def excitement_score(game):

    if game['gameStatus'] == 1:
        return -1
    
    if ("Half") in game['gameStatusText']:
        return -1
    
    home_score = game['homeTeam']['score']
    away_score = game['awayTeam']['score']
    rem = time_remaining(game)
    period = game['period']

    score_differential = abs(home_score - away_score)
    q4_bonus = 1 if period == 4 else 0
    overtime_bonus = 1 if period > 4 else 0

    w1, w2, w3, w4 = 5, 1, 1, 1.25

    excitement_score = (
        w1 * (1 / max(score_differential, 1)) +     # Closer scores are better
        w2 * (1 / max(rem, 1)) +                    # Less time remaining is better
        w3 * q4_bonus +                             # Boost for 4th quarter
        w4 * overtime_bonus                         # Boost for overtime
    )

    return excitement_score

# Rank the games by their excitement score
def most_exciting():
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()

    games_list = []
    for game in games:
        if game['gameStatus'] == 2:
            game_score = excitement_score(game)
            games_list.append((game, game_score))

    games_list.sort(key=lambda x: x[1], reverse=True)
    
    if games_list:
        top = games_list[0][0]

        if top['homeTeam']['teamName'] == "Trail Blazers":
            return "blazers"

        return top['homeTeam']['teamName'].lower().strip()
    else:
        return ('None')

# Return time remaining in seconds
def time_remaining(game):

    if game['gameStatus'] in (1, 3):
        return 0        # Game hasn't started or is already finished
    
    if "end q1" in game['gameStatusText'].lower():
        return 36
    
    if "end q2" or "half" in game['gameStatusText'].lower():
        return 24
    
    if "end q3" in game['gameStatusText'].lower():
        return 12
    
    if "end q4" in game['gameStatusText'].lower():
        return 0

    try:
        if game['gameClock'].startswith("PT"):
            match = re.match(r"PT(\d+)M(\d+)(?:\.\d+)?S", game['gameClock'])
            if match:
                minutes, seconds = int(match.group(1)), int(match.group(2))
        else:
            minutes, seconds = map(int, game['gameClock'].split(":"))
    except ValueError: # api glitches sometimes -- e.g. PT07M28.00S
        print(f"Invalid clock data for game {game}")
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

#def convert_time(time):
    


if __name__ == "__main__":
    app.run(port=5001)