from dataclasses import dataclass

@dataclass
class GameInfo:
    Id : int = 0
    SeriesId : int = 0
    Start : int = 0
    End : int = 0
    Winner : int = 0
    TossWinner : int = 0
    DescisionToBat : bool = True
    Margin : int = 0
    IsInnningsWin : bool = False
    IsWinByRuns : bool = False
    HomeTeamId : int = 0
    AwayTeamId : int = 0
    HomeTeamCapId : int = 0
    AwayTeamCapId : int = 0



@dataclass
class PlayerInfo:
    id : str = None
    name : str = None
    captain : bool = False
    Href : str = None

@dataclass
class TeamInfo:
    id : str = None
    name : str = None
    team : list = None
