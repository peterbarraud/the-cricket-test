from csv import DictReader

def get_playerscsv_dict():
    players_dict : dict = dict()
    with open('data/players.csv') as f:
        for row in DictReader(f):
            players_dict[row['id']] = row['name']
    return players_dict
