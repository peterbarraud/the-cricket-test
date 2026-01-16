from csv import reader as csvreader, writer as csvwriter,DictReader
from json import dumps
from libs.dataclasses import PlayerInfo,TeamInfo

def __get_teams_from_scorecard(scorecard):
    teams : dict = dict()
    for innings in scorecard:
        # batter details
        battingTeam = innings['batTeamDetails']
        team : TeamInfo = teams.get(battingTeam['batTeamId'],TeamInfo(battingTeam['batTeamId']))
        if team.Team is None:
            team.Team = list()
            teams[battingTeam['batTeamId']] = team
        for _,batter in battingTeam['batsmenData'].items():
            if not any(x.Id == batter['batId'] for x in team.Team):
                team.Team.append(PlayerInfo(batter['batId'],batter['batName']))
        # bowler details
        bowlingTeam = innings['bowlTeamDetails']
        team : TeamInfo = teams.get(bowlingTeam['bowlTeamId'],TeamInfo(bowlingTeam['bowlTeamId']))
        if team.Team is None:
            team.Team = list()
            teams[bowlingTeam['bowlTeamId']] = team
        for _,bowler in bowlingTeam['bowlersData'].items():
            if not any(x.Id == bowler['bowlerId'] for x in team.Team):
                team.Team.append(PlayerInfo(bowler['bowlerId'],bowler['bowlName']))


    return teams

def get_teams(teams_info,team1 : dict,team2 : dict,scoreCard):
    """
    Gets the team info for both teams in a dict by teamid
    
    :param teams_info: game_info_generator teamsInfo
    :param team1: Scorecard matchHeader - We need this to get the team Id (teams_info has only team name)
    :type team1: dict
    :param team2: Scorecard matchHeader - We need this to get the team Id (teams_info has only team name)
    :type team2: dict
    :para scoreCard - We need this because, seems that the teams_info is sometimes missiong players
    """
    team_dict : dict = dict()
    for team_info in teams_info[10][3]['children']:
        teamInfo = TeamInfo()
        teamInfo.Name = team_info[3]['children'][0][3]['children'][0]
        if team1['name'] == teamInfo.Name:
            teamInfo.Id = team1['id']
        elif  team2['name'] == teamInfo.Name:
            teamInfo.Id = team2['id']
        else:
            raise Exception("Team out not found")
        players : list = list()
        # playing 11
        for player_info in team_info[3]['children'][1][3]['children'][3]['children'][1][3]['children'][0]:
            players.append(PlayerInfo(player_info[2],player_info[3]['children'][0],'(c)' in player_info[3]['children'][1],player_info[3]['href']))
        # extras
        if team_info[3]['children'][1][3]['children'][3]['children'][1][3]['children'][1]:
            for player_info in team_info[3]['children'][1][3]['children'][3]['children'][1][3]['children'][1][3]['children'][1][3]['children']:
                players.append(PlayerInfo(player_info[2],player_info[3]['children'][0]))
        teamInfo.Team = players
        team_dict[teamInfo.Id] = teamInfo
    # the reason we get the teams from the scorecard is because we've found sometime the complete teams are not in the squad details
    if len(scoreCard) > 0:
        scoreCard_teams = __get_teams_from_scorecard(scoreCard)
        for id,team in team_dict.items():
            scoreCard_team = scoreCard_teams[id]
            if len(scoreCard_team.Team) > len(team.Team):
                team_ids = [int(x.Id) for x in team.Team]
                scorecard_ids = [x.Id for x in scoreCard_team.Team]
                missing_ids = [x for x in scorecard_ids if x not in team_ids]
                for missing_player in [x for x in scoreCard_team.Team if x.Id in missing_ids]:
                    team.Team.append(missing_player)
            # 
            # for player in team.Team:
            #     players = [x for x in scoreCard_team.Team if x.Id != player.Id]
            #     if len(players) == 1:
            #         team.Team.append(players[0])
            #     print()
    return team_dict


def get_teamscsv_dict():
    teams_dict : dict = dict()
    with open('data/teams.csv') as f:
        for row in DictReader(f):
            teams_dict[int(row['id'])] = row['name']
    return teams_dict

def make_teams_csv(teams_dict):
    with open('data/teams.csv','w') as f:
        csv_writer = csvwriter(f)
        all_teams : dict = dict()
        for id, team in teams_dict.items():
            if id not in all_teams.keys():
                all_teams[id] = []
            all_teams[id].append(team.Name)
        for i,j in teams_dict.items():
            if len(list(set(j))) != 1:
                raise Exception(f"Seems to have more than one entry for samne team id: {i}")
            else:
                csv_writer.writerow([i,j[0]])
