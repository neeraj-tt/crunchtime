from nba_api.live.nba.endpoints import scoreboard
import time
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["crunchtime"]
mycol = mydb["games"]

# print(json.dumps(box.game.get_dict(), indent=2))
# scoreFormat = "{time}\n{homeTeam}: {homeScore}\n{awayTeam}: {awayScore}"
while True:
    mycol.drop()
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