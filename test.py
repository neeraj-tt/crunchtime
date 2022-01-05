from datetime import date

from nba_api.stats.static import players
player_dict = players.get_players()

bron = [player for player in player_dict if player["full_name"] == "LeBron James"][0]
bron_id = bron['id']

from nba_api.stats.static import teams
team_dict = teams.get_teams()
TOR = [team for team in team_dict if team["full_name"] == "Toronto Raptors"][0]
TOR_id = TOR['id']

from nba_api.stats.endpoints import teamgamelog
raps = teamgamelog.TeamGameLog(team_id = TOR_id, season = '2021')
rapsDF = raps.get_data_frames()[0]

today = date.today()
d1 = today.strftime("%b %d, %Y")
print(d1)
# print(rapsDF.GAME_DATE)
if (rapsDF.GAME_DATE == "JAN 02, 2022") :
    print(rapsDF)
else :
    print("The Raptors did not play yesterday.")
