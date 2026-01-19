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
                'out':player.OutType.value,'fielders':"|".join([str(x) for x in player.Fielders]),
                'bowler':player.Bowler,'position':player.BattingPosition
            })

    def close(self):
        self.__f.close()

class PlayerCSV:
    def __init__(self,csv_file='data/players.csv'):
        self.__f = open(csv_file,'w',newline='')
        self.__players : dict = dict()
        self.__csv_writer = DictWriter(self.__f,['player','name','team','href'])
        self.__csv_writer.writeheader()

    def WriterRow(self, teamId : int, teamData : TeamInfo):
        player : PlayerInfo = None
        for player in teamData.Team:
            if saved_player := self.__players.get(player.Id,None):
                self.__players[player.Id].append(player)
            else:
                self.__csv_writer.writerow({'team':teamId,'player':player.Id,'name':player.Name,'href':player.Href})
                self.__players[player.Id] = list()
                self.__players[player.Id].append(player)

    def close(self):
        x = self.__players
        self.__f.close()
