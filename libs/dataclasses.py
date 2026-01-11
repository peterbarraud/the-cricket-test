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
    Team1Id : int = 0
    Team2Id : int = 0
    HomeTeamId : int = 0
    Team1CaptainId : int = 0
    Team2CaptainId : int = 0
    VenueId : int = 0

@dataclass
class PlayerInfo:
    Id : int = None
    Name : str = None
    Captain : bool = False
    Href : str = None

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
