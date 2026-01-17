from pathlib import Path
from json import load,dumps
from libs.dataclasses import TeamInfo,PlayerInfo
from re import match as rematch, sub as resub, findall as refindall

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

def __get_player_by_name(name : str,team : TeamInfo):
    player : PlayerInfo = None
    # 1. First, is the most basic check
    player_list = [x for x in team.Team if name.lower() == x.Name.lower()]
    if len(player_list) == 1:
        return player_list[0]
    else:
        # 2. Check if name is a single word (like Amla or Tendulkar)
        # The we're going to assume that is the only one in that team
        if ' ' not in name:
            player_list = [x for x in team.Team if name.lower() in x.Name.lower()]
            if len(player_list) == 1:
                return player_list[0]
            else:
                # 2.1. Check if the single name is a last name
                player_list = [x for x in team.Team if name == x.Name.split(' ')[-1]]
                if len(player_list) == 1:
                    return player_list[0]
                else:
                    pass
        else:
            # 3. We will check for first initial + last name. Like "V Kohli"
            g1 = rematch(r'^(.).+?(\S+?)$',name)
            first_init_last = f"{g1.groups()[0]} {g1.groups()[1]}"
            for player in team.Team:
                playername = resub(r'^Sir\s*','',player.Name)
                g2 = rematch(r'^(.).+?(\S+?)$',playername)
                if first_init_last == f"{g2.groups()[0]} {g2.groups()[1]}":
                    return player
                else:
                    # 4. If name is contained in Name
                    player_list = [x for x in team.Team if name.lower() in x.Name.lower()]
                    if len(player_list) == 1:
                        return player_list[0]

# handle name execptions
def __find_using_name_exceptions(name : str,bowling_team : PlayerInfo,play_name_exceptions : dict):
    if exception_names := play_name_exceptions.get(name,False):
        for exception_name in exception_names:
            retval = __get_player_by_name(exception_name,bowling_team)
            if retval:
                return retval
    return None
def __find_fielders(outdesc : str,bowling_team,play_name_exceptions : dict):
    fielders : list = list()
    g = rematch(r'^\s*(?:c|st)\s+(.+?)\s+b\s+(.+?)$',outdesc)
    if g:
        if len(g.groups()) == 2:
            fielder_name = g.groups()[0]
            fielder_name = fielder_name.replace('(sub)','')
            fielder = __get_player_by_name(fielder_name,bowling_team)
            if fielder:
                fielders.append(fielder)
            else:
                fielder = __find_using_name_exceptions(fielder_name,bowling_team,play_name_exceptions)
        else:
            pass
    else:
        pass
    return fielders

def __find_bowler(outdesc : str,bowling_team,play_name_exceptions : dict):
    if outdesc == 'c & b V Philander':
        pass
    bowler : PlayerInfo = None
    if outdesc.startswith('lbw ') or outdesc.startswith('b ') or outdesc.startswith('c & b ') or outdesc.startswith('hit wkt b ') or outdesc.startswith('hit wicket b '):
        name = outdesc.replace('hit wkt b ','').replace('lbw b ','').replace('c & b ','').replace('hit wicket b ','')
        # remove 'b ' but from start of the string ONLY
        name = resub(r'^b\s+','',name)
        bowler = __get_player_by_name(name,bowling_team)
        if not bowler:
            bowler = __find_using_name_exceptions(name,bowling_team,play_name_exceptions)
    else:
        g = rematch(r'^\s*(?:c|st)\s+(.+?)\s+b\s+(.+?)$',outdesc)
        if g:
            if len(g.groups()) == 2:
                bowler_name = g.groups()[1]
                bowler = __get_player_by_name(bowler_name,bowling_team)
                if not bowler:
                    bowler = __find_using_name_exceptions(bowler_name,bowling_team,play_name_exceptions)
            else:
                pass
        else:
            pass
    return bowler


def innings_info_generator(scorecard_data,match_teams,play_name_exceptions):
    for innings in scorecard_data:
        inning_number = innings['inningsId']
        battingTeamDetails = innings['batTeamDetails']
        bowlingTeamDetails = innings['bowlTeamDetails']
        battingTeam : TeamInfo = TeamInfo(battingTeamDetails['batTeamId'])
        bowlingTeam : TeamInfo = TeamInfo(bowlingTeamDetails['bowlTeamId'])
        battingTeam.Team = list()
        bowlingTeam.Team = list()
        for i, batter_data in battingTeamDetails['batsmenData'].items():
            outtype : str = batter_data['wicketCode']
            if outtype == '':
                if batter_data['outDesc'].lower() in ['not out','batting','retired not out']:
                    outtype = 'NOTOUT'
                elif batter_data['outDesc'].lower() in ['retired hurt','retired ill']:
                    outtype = 'RETIREDHURT'
                elif batter_data['outDesc'].lower().startswith('hit wicket'):
                    outtype = 'HITWICKET'
                elif batter_data['outDesc'].lower() in ['retired out']:
                    outtype = 'RETIREDOUT'
                else:
                    if batter_data['runs'] == 0 and batter_data.get('balls',0) == 0:
                        outtype = 'DIDNOTBAT'
            else:
                if outtype == 'RETD_HURT':
                    outtype = 'RETIREDHURT'
                elif outtype == 'RETD_OUT':
                    outtype = 'RETIREDOUT'
                elif outtype == 'HITWKT':
                    outtype = 'HITWICKET'
                elif outtype == 'ABSENT_HURT':
                    outtype = 'ABSENTHURT'
            
            bowler : PlayerInfo = PlayerInfo(batter_data.get('bowlerId',0))
            if outtype not in ['NOTOUT','DIDNOTBAT','RUNOUT','RETIREDHURT','ABSENTHURT','RETIREDOUT','HANDLED','OBSTRUCTION'] and bowler.Id == 0:
                bowler = __find_bowler(batter_data['outDesc'],match_teams[bowlingTeamDetails['bowlTeamId']],play_name_exceptions)
                if bowler is None:
                    raise Exception(f"Bowler not found: {batter_data['outDesc']}; Match: {innings['matchId']}")
            batter : PlayerInfo = PlayerInfo(batter_data['batId'])
            batter.Runs = batter_data['runs']
            batter.Balls = batter_data.get('balls',0)
            batter.Dots = batter_data.get('dots',0)
            batter.Fours = batter_data['fours']
            batter.Sixes = batter_data['sixes']
            batter.Mins = batter_data.get('mins',0)
            batter.Out = outtype
            batter.Bowler = bowler.Id if bowler else 0
            batter.BattingPosition = int(i.replace('bat_',''))
            fielders : list = list()
            batter.Fielders = list()
            if outtype in [ 'RUNOUT', 'CAUGHT', 'STUMPED','CAUGHTBOWLED']:
                pass
            fielder1 = batter_data.get('fielderId1',False)
            if fielder1:
                batter.Fielders.append(batter_data['fielderId1'])
            else:
                if outtype == 'CAUGHT' and fielder1 is False and len(fielders) > 0:
                    batter.Fielders.append(fielders[0].Id)
            fielder2 = batter_data.get('fielderId2',False)
            if fielder2:
                batter.Fielders.append(batter_data['fielderId2'])
            else:
                if outtype == 'CAUGHT' and fielder2 is False and len(fielders) > 1:
                    batter.Fielders.append(fielders[1].Id)
            fielder3 = batter_data.get('fielderId3',False)
            if fielder3:
                batter.Fielders.append(batter_data['fielderId3'])
            else:
                if outtype == 'CAUGHT' and fielder2 is False and len(fielders) > 2:
                    batter.Fielders.append(fielders[2].Id)
            # if we don't find any fields in the outers, we are going to put a 0
            # this way, we avoid NAN values in the dataframe
            if len(batter.Fielders) == 0:
                if outtype == 'CAUGHT':
                    pass
                batter.Fielders.append(0)
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
        
