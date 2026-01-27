import json
from csv import DictWriter,DictReader

from libs.logger import Logger
from libs.generators import game_info_generator,innings_info_generator
from libs.teams import get_teams,get_teamscsv_dict
from libs.gameinfo import get_game_info
from libs.dataclasses import GameInfo,TeamInfo,VenueInfo
from libs.playerinfo import get_playerscsv_dict,get_play_name_exceptions_dict
from libs.venueinfo import get_venue_info,get_venuecsv_dict
from libs.csvmaker import BattingCSV,PlayerCSV,GameCSV

def make_batting_data():
    play_name_exceptions = get_play_name_exceptions_dict()
    battingCSV = BattingCSV()
    c = 0
    for match_id,scorecard,teamsInfo in game_info_generator():
        # first we're going to make the match teams. we need this info for when the score doesn't give the bowler and fielder details
        match_teams = get_teams(teamsInfo,scorecard['matchHeader']['team1'],scorecard['matchHeader']['team2'],scorecard['scoreCard'])
        for inning_number,batting_team,bowling_team in innings_info_generator(scorecard['scoreCard'],match_teams,play_name_exceptions):
            battingCSV.WriterRow(match_id,inning_number,batting_team)
        c += 1
        if c/110 == int(c/110):
            print(c)
    battingCSV.close()

def make_player_data():
    playerCSV = PlayerCSV()
    c = 0
    for match_id,scorecard,teamsInfo in game_info_generator():
        # first we're going to make the match teams. we need this info for when the score doesn't give the bowler and fielder details
        for id,team in get_teams(teamsInfo,scorecard['matchHeader']['team1'],scorecard['matchHeader']['team2'],scorecard['scoreCard']).items():
            playerCSV.WriterRow(id,team)
        c += 1
        if c/100 == int(c/100):
            print(c)

    playerCSV.close()

def make_game_data():
    c = 0
    gameCSV = GameCSV()
    for match_id,scorecard,teamsInfo in game_info_generator():
        c += 1
        print(f"{c}: {match_id}")
        game_info : GameInfo = get_game_info(scorecard['matchHeader'],teamsInfo[10][3]['children'])
        if game_info.Team1Captain == 0:
            raise Exception(f"{match_id} - Issue with team captain Team1Captain = 0")
        if game_info.Team2Captain == 0:
            raise Exception(f"{match_id} - Issue with team captain Team2Captain = 0")
        gameCSV.WriterRow(game_info)
    
    gameCSV.close()

def main():
    pass

if __name__ == "__main__":
    print()
    main()
    print('DONE')
