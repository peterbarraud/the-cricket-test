from csv import DictWriter
from libs.dataclasses import TeamInfo,PlayerInfo

class BattingCSV:
    def __init__(self,csv_file='data/batting.csv'):
        self.__f = open(csv_file,'w',newline='')
        field_names = ['gameid,innings,team,batter,position,runs,balls,fours,sixes,out,fielders,bowler']
        self.__csv_writer = DictWriter(self.__f,field_names)

    def WriterRow(self, game_id : int, innings_number : int, battingTeamData : TeamInfo):
        player : PlayerInfo = None
        for player in battingTeamData.Team:
            row : dict = dict()
            row['gameid'] = game_id
            row['innings'] = innings_number
            row['team'] = battingTeamData.Id
            row['batter'] = player.Id
            row['runs'] = player.Runs
            row['balls'] = player.Balls
            row['fours'] = player.Fours
            row['sixes'] = player.Sixes
            row['out'] = player.Out
            row['fielders'] = "|".join([str(x) for x in player.Fielders])
            row['bowler'] = player.Bowler
            row['position'] = player.BattingPosition
            self.__csv_writer.writerow(row)

    


    def close(self):
        self.__f.close()