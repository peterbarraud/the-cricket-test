import json
from csv import DictWriter

from libs.logger import Logger
from libs.generators import game_info_generator,innings_info_generator
from libs.teams import get_teams,get_teamscsv_dict
from libs.gameinfo import get_game_info
from libs.dataclasses import GameInfo,TeamInfo,VenueInfo
from libs.playerinfo import get_playerscsv_dict,get_play_name_exceptions_dict
from libs.venueinfo import get_venue_info,get_venuecsv_dict

from libs.csvmaker import BattingCSV

def __clean_logs(filename):
    with open(filename,'w') as f:
        f.write('')
def main():
    __clean_logs('logs/fielders.not.found.log')


    play_name_exceptions = get_play_name_exceptions_dict()
    battingCSV = BattingCSV()
    log = Logger()
    c = 0
    # playerscsv_dict : dict = get_playerscsv_dict()
    # venuecsv_dict : dict = get_venuecsv_dict()
    # batting_csv.WriteLn('match,innings,team,player,runs,out,\n')
    for match_id,scorecard,teamsInfo in game_info_generator():
        # first we're going to make the match teams. we need this info for when the score doesn't give the bowler and fielder details
        match_teams = get_teams(teamsInfo,scorecard['matchHeader']['team1'],scorecard['matchHeader']['team2'],scorecard['scoreCard'])
        for i,j in match_teams.items():
            if len(j.Team) < 11:
                raise Exception("Team size is {len(j.Team)}")
        for inning_number,batting_team,bowling_team in innings_info_generator(scorecard['scoreCard'],match_teams,play_name_exceptions):
            battingCSV.WriterRow(match_id,inning_number,batting_team)
        c += 1
        if c/110 == int(c/110):
            print(c)
    battingCSV.close()

if __name__ == "__main__":
    print()
    main()
    print('DONE')
