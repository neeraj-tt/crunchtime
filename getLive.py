from nba_api.live.nba.endpoints import scoreboard
import time
import pymongo
import certifi

ca = certifi.where()
myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.aeen5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=ca)
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