from libs.dataclasses import PlayerInfo,TeamInfo
from csv import reader as csvreader, writer as csvwriter

def get_teams(teams_info,team1 : dict,team2 : dict):
    team_dict : dict = dict()
    for team_info in teams_info:
        teamInfo = TeamInfo()
        teamInfo.name = team_info[3]['children'][0][3]['children'][0]
        if team1['name'] == teamInfo.name:
            teamInfo.id = team1['id']
        elif  team2['name'] == teamInfo.name:
            teamInfo.id = team2['id']
        else:
            raise Exception("Team out not found")
        players : list = list()
        for player_info in team_info[3]['children'][1][3]['children'][3]['children'][1][3]['children'][0]:
            players.append(PlayerInfo(player_info[2],player_info[3]['children'][0],'(c)' in player_info[3]['children'][1],player_info[3]['href']))
        teamInfo.team = players
        team_dict[teamInfo.id] = teamInfo
    return team_dict


def get_teams_dict():
    teams_dict : dict = dict()
    with open('data/teams.csv') as f:
        for row in csvreader(f):
            teams_dict[int(row[0])] = row[1]
    return teams_dict

def make_teams_csv(teams_dict):
    with open('data/teams.csv','w') as f:
        csv_writer = csvwriter(f)
        all_teams : dict = dict()
        for id, team in teams_dict.items():
            if id not in all_teams.keys():
                all_teams[id] = []
            all_teams[id].append(team.name)
        for i,j in teams_dict.items():
            if len(list(set(j))) != 1:
                raise Exception(f"Seems to have more than one entry for samne team id: {i}")
            else:
                csv_writer.writerow([i,j[0]])
