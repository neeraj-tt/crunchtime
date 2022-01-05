from typing import Mapping
from flask import Flask
from flask import render_template

from datetime import datetime, timezone
from dateutil import parser
import time

from nba_api.live.nba.endpoints import scoreboard

app = Flask(__name__)

@app.route("/")
def index():
    datetime_today = datetime.today()
    pret = datetime_today.strftime("%b %d, %Y")
    arr = getGames()
    
    return render_template("index.html", title = "Crunchtime", pret=pret, games=arr)

def getGames():
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()
    arr = []
    curr = {}
    for game in games:
        curr = {
            "time": game['gameStatusText'],
            "homeTeam": game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName'],
            "homeScore": game['homeTeam']['score'],
            "awayTeam": game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'], 
            "awayScore": game['awayTeam']['score']
        }
        arr.append(curr)
    return arr

if __name__ == "__main__":
    # app.run(threaded=True)
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)

# print(json.dumps(box.game.get_dict(), indent=2))
# scoreFormat = "{time}\n{homeTeam}: {homeScore}\n{awayTeam}: {awayScore}"
# for x in range(1):
#     board = scoreboard.ScoreBoard()
#     games = board.games.get_dict()
#     for game in games:
#         game = {
#             "time": game['gameStatusText'],
#             "homeTeam": game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName'],
#             "homeScore": game['homeTeam']['score'],
#             "awayTeam": game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'], 
#             "awayScore": game['awayTeam']['score']
#         }
#         print(game)
#         #print(scoreFormat.format(time = game['gameStatusText'], homeTeam=game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName'], homeScore = game['homeTeam']['score'], awayTeam=game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'], awayScore=game['awayTeam']['score']))
#     time.sleep(5)
    
