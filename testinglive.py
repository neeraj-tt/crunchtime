from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
import time
import json
import pymongo

import redis

r = redis.StrictRedis(host="localhost", port=6379, db=0)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["crunchtime"]
mycol = mydb["games"]

f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 

board = scoreboard.ScoreBoard()
print("ScoreBoardDate: " + board.score_board_date)
games = board.games.get_dict()
for game in games:
    gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
    print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))

from nba_api.live.nba.endpoints import boxscore


# print(json.dumps(box.game.get_dict(), indent=2))
scoreFormat = "{time}\n{homeTeam}: {homeScore}\n{awayTeam}: {awayScore}"
while True:
    mycol.drop()
    #box = boxscore.BoxScore('0022100566')  
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()
    for game in games:
        game = {
            "time": game['gameStatusText'],
            "homeTeam": game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName'],
            "homeScore": game['homeTeam']['score'],
            "awayTeam": game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'], 
            "awayScore": game['awayTeam']['score'],
            "period": game['period'],
            "rem": game['gameClock']
        }
        print(game)
        mycol.insert_one(game)
        #print(scoreFormat.format(time = game['gameStatusText'], homeTeam=game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName'], homeScore = game['homeTeam']['score'], awayTeam=game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'], awayScore=game['awayTeam']['score']))
    time.sleep(5)

# box = boxscore.BoxScore('0022100566')  
# game = box.game.get_dict()   
# print(json.dumps(game, indent=2))
# print(game['homeTeam']['score'])

# players = box.home_team.get_dict()['players']
# f = "{player_id}: {name}: {points} PTS"
# for player in players:
#     print(f.format(player_id=player['personId'],name=player['name'],points=player['statistics']['points']))