
from libs.logger import Logger
from libs.generators import game_info_generator
from libs.teams import get_teams,get_teams_dict
from libs.gameinfo import get_game_info
from libs.dataclasses import GameInfo

def main():
    logger : Logger = Logger()
    c = 0
    players_dict : dict = dict()
    for scorecard,teamsInfo in game_info_generator():
        c += 1
        game_info : GameInfo = get_game_info(scorecard['matchHeader'])
        teams_dict = get_teams(teamsInfo[10][3]['children'],scorecard['matchHeader']['team1'],scorecard['matchHeader']['team2'])
        if teams_dict.get(game_info.HomeTeamId):
            #TODO:  not sure why the following check is required
            if cap_list := [x for x in teams_dict[game_info.HomeTeamId].team if x.captain]:
                game_info.HomeTeamCapId = cap_list[0].id
        if teams_dict.get(game_info.AwayTeamId):
            if cap_list := [x for x in teams_dict[game_info.AwayTeamId].team if x.captain]:
                game_info.AwayTeamCapId = cap_list[0].id
        for i, j in teams_dict.items():
            for k in j.team:
                if not players_dict.get(k.id,False):
                    players_dict[k.id] = k
        if c/100 == int(c/100):
            print(c)


        # teams_dict = get_teams(teamsInfo[10][3]['children'],scorecard['matchHeader']['team1'],scorecard['matchHeader']['team2'])
    with open('data/players.csv','w') as f:
        f.write("id,name,href\n")
        for i,j in players_dict.items():
            f.write(f'{i},{j.name},{j.Href}\n')
    logger.close()

    print()

if __name__ == "__main__":
    print()
    main()
    print('DONE')