from csv import DictWriter
from libs.dataclasses import TeamInfo,PlayerInfo,GameInfo
from libs.csvnames import CSVName
from io import TextIOWrapper

class CSVBase:
    def __init__(self,csv_file : str,field_names : list):
        self.__f : TextIOWrapper = open(csv_file,'w',newline='')
        x = self.__f
        self.__csv_writer = DictWriter(self.__f,field_names)
        self.__csv_writer.writeheader()

    def WriteRow(self,row : dict):
        self.__csv_writer.writerow(row)

    def close(self):
        print(f'CSV saved at: {self.__f.name}')
        self.__f.close()


class BattingCSV(CSVBase):
    def __init__(self,csv_file=f'data/{CSVName.Batting.name.lower()}.csv'):
        super().__init__(csv_file,['gameid','innings','team','batter','position',
                       'runs','balls','fours','sixes','out','fielders','bowler'])

    def WriterRow(self, game_id : int, innings_number : int, battingTeamData : TeamInfo):
        player : PlayerInfo = None
        for player in battingTeamData.Team:
            super().WriteRow({'gameid':game_id,'innings':innings_number,'team':battingTeamData.Id,'batter':player.Id,
                'runs':player.Runs,'balls':player.Balls,'fours':player.Fours,'sixes':player.Sixes,
                'out':player.OutType.value,'fielders':"|".join([str(x) for x in player.Fielders]),
                'bowler':player.Bowler,'position':player.BattingPosition
            })


class PlayerCSV(CSVBase):
    def __init__(self,csv_file=f'data/{CSVName.Players.name.lower()}.csv'):
        super().__init__(csv_file,['gameid','innings','team','batter','position',
                       'runs','balls','fours','sixes','out','fielders','bowler'])
        self.__players : dict = dict()

    def WriterRow(self, teamId : int, teamData : TeamInfo):
        player : PlayerInfo = None
        for player in teamData.Team:
            if saved_player := self.__players.get(player.Id,None):
                self.__players[player.Id].append(player)
            else:
                super().WriteRow({'team':teamId,'player':player.Id,'name':player.Name,'href':player.Href})
                self.__players[player.Id] = list()
                self.__players[player.Id].append(player)

class GameCSV(CSVBase):
    def __init__(self,csv_file=f'data/{CSVName.Games.name.lower()}.csv'):
        
        super().__init__(csv_file,['game','series','start','end','winner','tosswinner','descisiontobat',
                                   'margin','isinnningswin','iswinbyruns','team1','team2','hometeam',
                                   'team1captain','team2captain','venue'])

    def WriterRow(self, gameData : GameInfo):
        super().WriteRow({'game':gameData.Id,'series':gameData.Series,'start':gameData.Start,
                                    'end':gameData.End,'winner':gameData.Winner,'tosswinner':gameData.TossWinner,
                                    'descisiontobat':gameData.DescisionToBat,'margin':gameData.Margin,
                                    'isinnningswin':gameData.IsInningsWin,'iswinbyruns':gameData.IsWinByRuns,
                                    'team1':gameData.Team1,'team2':gameData.Team2,'hometeam':gameData.HomeTeam,
                                   'team1captain':gameData.Team1Captain,'team2captain':gameData.Team2Captain,'venue':gameData.Venue})
        

class TeamCSV(CSVBase):
    def __init__(self,csv_file=f'data/{CSVName.Teams.name.lower()}.csv'):
        super().__init__(csv_file,['id','name','shortname'])

    def WriterRow(self, teamData : TeamInfo):
        super().WriteRow({'id':teamData.Id,'name':teamData.Name,'shortname':teamData.ShortName})
        
        


