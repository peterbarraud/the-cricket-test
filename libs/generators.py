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
    g1 = rematch(r'^(.).+?(\S+?)$',name)
    shortName1 = f"{g1.groups()[0]} {g1.groups()[1]}"
    if len(name.split(' ')) == 1:
        shortName1 = name
    for player in team.Team:
        playername = resub(r'^Sir\s*','',player.Name)
        g2 = rematch(r'^(.).+?(\S+?)$',playername)
        shortName2 = f"{g2.groups()[0]} {g2.groups()[1]}"
        if shortName1 == shortName2:
            return player
    else:
        player_list = [x for x in team.Team if x.Name.lower().endswith(f" {name.lower()}")]
        if len(player_list) == 1:
            return player_list[0]
        else:
            player_list = [x for x in team.Team if name.lower() in x.Name.lower()]
            if len(player_list) == 1:
                return player_list[0]
            else:
                lastname = rematch(r'^(.).+?(\S+?)$',name).groups()[1]
                player_list = [x for x in team.Team if x.Name.lower().endswith(f" {lastname}") or x.Name.lower().endswith(f" {lastname.lower().replace("'","")}")]
                if len(player_list) == 1:
                    return player_list[0]
                else:
                    print(name)
    #     p.Name
    # shortName = f"{g.groups()[0]} {g.groups()[1]}"
    # lastName = g.groups()[1]
    # player_list = [x for x in team.Team if x.Name.lower() == name
    #                or name.lower() in x.Name.lower()
    #                or name.lower() in x.ShortName.lower()
    #                or shortName.lower() in x.ShortName.lower()
    #                or x.Name.lower().endswith(lastName.lower())]
    # if len(player_list) == 1:
    #     player = player_list[0]
    # else:
    #     print()
    
    # shortName = f"{g.groups()[0]} {g.groups()[1]}"
    # if shortName != name:
    #     print()
    # player_list = [x for x in team.Team if x.ShortName.lower() in name]
    # if len(player_list) == 1:
    #     player = player_list[0]
    # else:
    #     first_name,last_name = name.split()[0],name.split()[-1]
    #     player_list = [x for x in team.Team if last_name.lower() in x.Name.lower()]
    #     if len(player_list) == 1:
    #         player = player_list[0]
    #     elif len(player_list) > 1:
    #         first_name_list = [x for x in team.Team if x.Name.lower().startswith(first_name.lower())]
    #         if len(first_name_list) == 1:
    #             player = first_name_list[0]
    #         else:
    #             print()
    #     else:
    #         print()

def __find_outers(outdesc : str, bowlersData,bowling_team):
    bowler : PlayerInfo = None
    fielders : list = list()
    if outdesc.startswith('lbw ') or outdesc.startswith('b ') or outdesc.startswith('c & b '):
        name = outdesc.replace('lbw b ','').replace('c & b ','').replace('b ','')
        bowler = __get_player_by_name(name,bowling_team)
        if bowler is None:
            print()
    else:
        g = rematch(r'^\s*(?:c|st)\s+(.+?)\s+b\s+(.+?)$',outdesc)
        if g:
            if len(g.groups()) == 2:
                fielder_name = g.groups()[0]
                bowler_name = g.groups()[1]
                bowler = __get_player_by_name(bowler_name,bowling_team)
                #TODO: For now, we are going to ignore catches by substitute players
                if not fielder_name.startswith('(sub)'):
                    fielder = __get_player_by_name(fielder_name,bowling_team)
                    if fielder:
                        fielders.append(fielder)
                    else:
                        print()
            else:
                print()
        else:
            print()
    return bowler,fielders


def innings_info_generator(scorecard_data,match_teams):
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
            
            #TODO: Check for no bowler
            bowler : PlayerInfo = PlayerInfo(batter_data.get('bowlerId',0))
            if outtype not in ['NOTOUT','DIDNOTBAT','RUNOUT','RETIREDHURT','ABSENTHURT','RETIREDOUT'] and bowler.Id == 0:
                bowler,fielders = __find_outers(batter_data['outDesc'],bowlingTeamDetails['bowlersData'],match_teams[bowlingTeamDetails['bowlTeamId']])
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
            # if we don't find any fields in the outers, we are going to put a 0
            # this way, we avoid NAN values in the dataframe
            if len(batter.Fielders) == 0:
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
        
