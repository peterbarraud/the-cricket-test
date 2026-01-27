from dataclasses import dataclass
from libs.outtype import OutType

@dataclass
class GameInfo:
    Id : int = 0
    Series : int = 0
    Start : int = 0
    End : int = 0
    Winner : int = 0
    TossWinner : int = 0
    DescisionToBat : bool = True
    Margin : int = 0
    IsInningsWin : bool = False
    IsWinByRuns : bool = False
    Team1 : int = 0
    Team2 : int = 0
    HomeTeam : int = 0
    Team1Captain : int = 0
    Team2Captain : int = 0
    Venue : int = 0

    def __eq__(self, other):
        otherObject : GameInfo = other
        isDifferent = 0
        if self.Id != otherObject.Id:
            print('game different')
            isDifferent += 1
        if self.Series != otherObject.Series:
            print('series different')
            isDifferent += 1
        if self.Start != otherObject.Start:
            print('start different')
            isDifferent += 1
        if self.End != otherObject.End:
            print('end different')
            isDifferent += 1
        if self.Winner != otherObject.Winner:
            print('winner different')
            isDifferent += 1
        if self.TossWinner != otherObject.TossWinner:
            print('toss winner different')
            isDifferent += 1
        if self.DescisionToBat != otherObject.DescisionToBat:
            print('DescisionToBat different')
            isDifferent += 1
        if self.Margin != otherObject.Margin:
            print('margin different')
            isDifferent += 1
        if self.IsInningsWin != otherObject.IsInningsWin:
            print('IsInningsWin different')
            isDifferent += 1
        if self.IsWinByRuns != otherObject.IsWinByRuns:
            print('IsWinByRuns different')
            isDifferent += 1
        if self.Team1 != otherObject.Team1:
            print('Team1 different')
            isDifferent += 1
        if self.Team2 != otherObject.Team2:
            print('Team2 different')
            isDifferent += 1
        if self.HomeTeam != otherObject.HomeTeam:
            print('HomeTeam different')
            isDifferent += 1
        if self.Team1Captain != otherObject.Team1Captain:
            print('Team1Captain different')
            isDifferent += 1
        if self.Team2Captain != otherObject.Team2Captain:
            print('Team2Captain different')
            isDifferent += 1
        if self.Venue != otherObject.Venue:
            print('Venue different')
            isDifferent += 1
        return isDifferent == 0


@dataclass
class PlayerInfo:
    Id : int = None
    Name : str = None
    Captain : bool = False
    Href : str = None
    Runs : int = 0
    Balls : int = 0
    Dots : int = 0
    Fours : int = 0
    Sixes : int = 0
    Mins : int = 0
    OutType = OutType.NOTOUT
    Bowler : int = 0
    BattingPosition : int = 0
    Fielders : list = None



@dataclass
class TeamInfo:
    Id : int = 0
    Name : str = None
    Team : list = None

@dataclass
class VenueInfo:
    Id : int = 0
    Name : str = None
    City : str = None
    Country : int = 0
