import json
from csv import DictWriter,DictReader

from libs.logger import Logger
from libs.generators import game_info_generator,innings_info_generator
from libs.teams import get_teams,get_teamscsv_dict,get_team_info,get_teams_by_name
from libs.gameinfo import get_game_info
from libs.dataclasses import GameInfo,TeamInfo,VenueInfo
from libs.playerinfo import get_playerscsv_dict,get_play_name_exceptions_dict
from libs.venueinfo import get_venue_info,get_venuecsv_dict
from libs.csvmaker import BattingCSV,PlayerCSV,GameCSV,TeamCSV,VenueCSV

def make_batting_data():
    play_name_exceptions = get_play_name_exceptions_dict()
    battingCSV = BattingCSV()
    c = 0
    for match_id,scorecard,teamsInfo in game_info_generator():
        # first we're going to make the match teams. we need this info for when the score doesn't give the bowler and fielder details
        match_teams = get_teams(teamsInfo,scorecard['matchHeader']['team1'],scorecard['matchHeader']['team2'],scorecard['scoreCard'])
        for inning_number,batting_team,bowling_team in innings_info_generator(scorecard['scoreCard'],match_teams,play_name_exceptions):
            battingCSV.WriteRow(match_id,inning_number,batting_team)
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
            playerCSV.WriteRow(id,team)
        c += 1
        if c/100 == int(c/100):
            print(c)

    playerCSV.close()

def get_config():
    with open('libs/config.json') as f:
        return json.load(f)


def make_team_and_venue_data():
    """
    Makes the teams.csv and venues.csv
    """
    c = 0
    # team_id_list : list = list()
    ven_id_list : list = list()
    teams_dict : dict = dict()
    teamCSV = TeamCSV()
    venueCSV = VenueCSV()
    teams_not_found : dict = dict()
    for _,scorecard,_ in game_info_generator():
        c += 1
        if c % 100 == 0:
            print(c)
        for teamId,teamInfo in get_team_info(scorecard).items():
            if teamId not in teams_dict.values():
                teamCSV.WriteRow(teamInfo)
                teams_dict[teamInfo.Name] = teamInfo.Id

        venue_info : dict = scorecard['matchHeader']['venue']
        id : int = int(venue_info['id'])
        if id not in ven_id_list:
            venueInfo : VenueInfo = VenueInfo(id,venue_info['name'],venue_info['city'])
            if country := teams_dict.get(venue_info['country'],None):
                venueInfo.Country = country
                venueCSV.WriteRow(venueInfo)
                ven_id_list.append(id)
                teams_not_found.pop(id, None)
            else:
                # if a game is played on a neutral venue, then that country may not have been added to the teams_dict
                # in most cases, it will get added at some point
                # but there are some cases, like UAE which never played a game. So, they won't
                # so, for now we are not going to add these venues to the CSV
                venueInfo.CountryName = venue_info['country']
                teams_not_found[id] = venueInfo

    if len(teams_not_found.keys()) > 0:
        for id,not_found_venue_info in teams_not_found.items():
            if not teams_dict.get(not_found_venue_info.CountryName,False):
                new_team_id : int = max(teams_dict.values()) + 1
                teamCSV.WriteRow(TeamInfo(new_team_id,not_found_venue_info.CountryName,not_found_venue_info.CountryName))
                teams_dict[not_found_venue_info.CountryName] = new_team_id
            not_found_venue_info.Country = teams_dict[not_found_venue_info.CountryName]
            venueCSV.WriteRow(not_found_venue_info)
    # we are also going to add one row for neutral venue (id=0)
    # this will help later when we search for the country name for a venue (id)
    teamCSV.WriteRow(TeamInfo(0,'Neutral'))
    venueCSV.close()
    teamCSV.close()

def _get_teams_dict(csv_file):
    csv_dict : dict = dict()
    with open(csv_file) as f:
        for row in DictReader(f):
            csv_dict[row['id']] = TeamInfo(row['id'],row['name'])
    return csv_dict

def _get_venues_dict(csv_file):
    csv_dict : dict = dict()
    with open(csv_file) as f:
        for row in DictReader(f,delimiter='|'):
            csv_dict[row['id']] = VenueInfo(Id=row['id'],Name=row['name'],City=row['city'],Country=row['country'])
    return csv_dict
    
def compare_old_new_csv():
    old_csv_dict : dict = _get_venues_dict('data/venues.csv')
    new_csv_dict : dict = _get_venues_dict('data/venues.new.csv')
    for old_id,old_item in old_csv_dict.items():
        new_item = new_csv_dict.get(old_id,None)
        if new_item:
            if old_item != new_item:
                print(f"venue not same: {old_id}")
        else:
            print(f"new venue not found: {old_id}")

    for new_id,new_item in new_csv_dict.items():
        old_item = old_csv_dict.get(new_id,None)
        if old_item:
            if old_item != new_item:
                print(f"venue not same: {new_item.Name}")
        else:
            print(f"old venue not found: {new_item.Name}")


    pass

def main():
    make_team_and_venue_data()
    # compare_old_new_csv()

if __name__ == "__main__":
    print()
    main()
    print('DONE')
