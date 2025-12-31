from csv import DictReader
from dataclasses import dataclass
import pickle
from re import search as research, IGNORECASE

@dataclass
class PlayerInfo:
    ID : int = None
    ObjectID : int = None
    Name : str = None
    DateOfBirth : str = None
    DateOfDeath : str = None
    BattingStyle : str = None
    BowlingStyle : str = None
    CountryID : int = None

def store_players_info():
    with open('data/players_info.csv') as f:
        players_dict : dict = dict()
        for row in DictReader(f):
            playerInfo = PlayerInfo(row['player_id'],row['player_object_id'],
                                    row['player_name'], row['dob'], row['dod'],
                                    row['batting_style'], row['bowling_style'], row['country_id'])
            players_dict[int(row['player_id'])] = playerInfo
        with open('data/players_info.dict', 'wb') as pi:
            pickle.dump(players_dict,pi)

def get_player_info_by_id(player_id : int):
    with open('data/players_info.dict', 'rb') as pi:
        players_dict : dict = pickle.load(pi)
        return players_dict.get(player_id, 'Not found')

def get_player_info_by_name(player_name : int):
    with open('data/players_info.dict', 'rb') as pi:
        players_dict : dict = pickle.load(pi)
        return [x for x in players_dict.values() if research(player_name,x.Name,flags=IGNORECASE)]


if __name__ == "__main__":
    print()
    print(get_player_info_by_name('Gavas'))
    # store_players_info()
    print('DONE')
