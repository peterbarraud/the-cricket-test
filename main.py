import json

from libs.logger import Logger
from libs.generators import game_info_generator,innings_info_generator
from libs.teams import get_teams,get_teamscsv_dict
from libs.gameinfo import get_game_info
from libs.dataclasses import GameInfo,TeamInfo,VenueInfo
from libs.playerinfo import get_playerscsv_dict
from libs.venueinfo import get_venue_info,get_venuecsv_dict


def main():
    teamscsv_dict = get_teamscsv_dict()
    logger : Logger = Logger()
    c = 0
    playerscsv_dict : dict = get_playerscsv_dict()
    venuecsv_dict : dict = get_venuecsv_dict()
    for scorecard,teamsInfo in game_info_generator():
        teams = get_teams(teamsInfo,scorecard['matchHeader']['team1'],scorecard['matchHeader']['team2'])
        for innings_info in innings_info_generator(scorecard['scoreCard']):
            pass
        c += 1
        if c/110 == int(c/110):
            print(c)

    logger.close()
    print()

if __name__ == "__main__":
    print()
    main()
    print('DONE')
