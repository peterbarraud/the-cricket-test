from csv import DictReader

def get_playerscsv_dict():
    players_dict : dict = dict()
    with open('data/players.csv') as f:
        return {row['id']:row['name'] for row in DictReader(f)}
            
    return players_dict

def get_play_name_exceptions_dict():
    d : dict = dict()
    with open('data/player.name.exceptions.csv') as f:
        for row in DictReader(f):
            names = row['name'].split("|")
            d[row['altname']] = names
    return d
