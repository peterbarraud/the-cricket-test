from csv import DictWriter
from libs.dataclasses import TeamInfo,PlayerInfo

class BattingCSV:
    def __init__(self,csv_file='data/batting.csv'):
        self.__f = open(csv_file,'w',newline='')
        field_names = ['gameid','innings','team','batter','position',
                       'runs','balls','fours','sixes','out','fielders','bowler']
        self.__csv_writer = DictWriter(self.__f,field_names)
        self.__csv_writer.writeheader()

    def WriterRow(self, game_id : int, innings_number : int, battingTeamData : TeamInfo):
        player : PlayerInfo = None
        for player in battingTeamData.Team:
            self.__csv_writer.writerow({'gameid':game_id,'innings':innings_number,'team':battingTeamData.Id,'batter':player.Id,
                'runs':player.Runs,'balls':player.Balls,'fours':player.Fours,'sixes':player.Sixes,
                'out':player.Out,'fielders':"|".join([str(x) for x in player.Fielders]),
                'bowler':player.Bowler,'position':player.BattingPosition
            })

    


    def close(self):
        self.__f.close()