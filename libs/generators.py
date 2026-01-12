from pathlib import Path
from json import load,dumps
from libs.dataclasses import TeamInfo,PlayerInfo
from libs.logger import Logger

def include_game(game_description : str):
    if 'practice match' in game_description.lower():
        return False
    elif 'warm-up match' in game_description.lower():
        return False
    elif '4 day game' in game_description.lower():
        return False
    elif 'Tour Match' in game_description.lower():
        return False
    else:
        return True

def get_abandoned_game_list():
    with open('data/abandoned.games') as f:
        return [int(x.strip()) for x in f]

def game_info_generator():
    abandoned_game_list = get_abandoned_game_list()
    for path in [p for p in Path('data/game.jsons').iterdir() if p.is_file()]:
        scorecard = None
        match_info = None
        with open(path) as f:
            j = load(f)
            scorecard = j['children'][0][3]['scorecardApiData']
            if scorecard['matchHeader']['matchId'] in abandoned_game_list:
                continue
            # strange exception
            # "England lions" just seems to come into the mix.
            # Need to exclude
            if 'england lions' not in scorecard['matchHeader']['team1']['name'].lower() and 'england lions' not in scorecard['matchHeader']['team2']['name']:
                if include_game(scorecard['matchHeader']['matchDescription']):
                    match_info = j['children'][1]
                    match_id = scorecard['matchHeader']['matchId']
                    yield match_id,scorecard,match_info

def innings_info_generator(scorecard_data):
    for innings in scorecard_data:
        match_id = innings['matchId']
        inning_number = innings['inningsId']
        battingTeamDetails = innings['batTeamDetails']
        bowlingTeamDetails = innings['bowlTeamDetails']
        battingTeam : TeamInfo = TeamInfo(battingTeamDetails['batTeamId'])
        bowlingTeam : TeamInfo = TeamInfo(bowlingTeamDetails['bowlTeamId'])
        battingTeam.Team = list()
        bowlingTeam.Team = list()
        for i, batter_data in battingTeamDetails['batsmenData'].items():
            batter : PlayerInfo = PlayerInfo(batter_data['batId'])
            batter.Runs = batter_data['runs']
            batter.Balls = batter_data.get('balls',0)
            batter.Dots = batter_data.get('dots',0)
            batter.Fours = batter_data['fours']
            batter.Sixes = batter_data['sixes']
            batter.Mins = batter_data.get('mins',0)
            batter.Out = batter_data['wicketCode']
            batter.Bowler = batter_data.get('bowlerId',0)
            batter.BattingPosition = int(i.replace('bat_',''))
            batter.Fielders = list()
            fielder1 = batter_data.get('fielderId1',False)
            if fielder1:
                batter.Fielders.append(batter_data['fielderId1'])
            fielder2 = batter_data.get('fielderId2',False)
            if fielder2:
                batter.Fielders.append(batter_data['fielderId2'])
            fielder3 = batter_data.get('fielderId3',False)
            if fielder3:
                batter.Fielders.append(batter_data['fielderId3'])
            battingTeam.Team.append(batter)
        for i, bowler_data in bowlingTeamDetails['bowlersData'].items():
            bowler : PlayerInfo = PlayerInfo(bowler_data['bowlerId'])
            bowler.Overs = bowler_data['overs']
            bowler.Maidens = bowler_data['maidens']
            bowler.Runs = bowler_data['runs']
            bowler.Wickets = bowler_data['wickets']
            bowlingTeam.Team.append(bowler)


        # for i, bowler in bowlingTeamDetails['bowlersData'].items():
        #     batting_position = int(i.replace('bat_',''))
        yield inning_number,battingTeam,bowlingTeam
        
