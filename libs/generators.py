from pathlib import Path
from json import load

def include_game(game_description : str):
    if 'practice match' in game_description.lower():
        return False
    elif 'warm-up match' in game_description.lower():
        return False
    elif '4 day game' in game_description.lower():
        return False
    elif 'Tour Match' in game_description.lower():
        return False
    else:
        return True

def game_info_generator():
    for path in [p for p in Path('data/game.jsons').iterdir() if p.is_file()]:
        scorecard = None
        match_info = None
        with open(path) as f:
            j = load(f)
            scorecard = j['children'][0][3]['scorecardApiData']
            # strange exception
            # "England lions" just seems to come into the mix.
            # Need to exclude
            if 'england lions' not in scorecard['matchHeader']['team1']['name'].lower() and 'england lions' not in scorecard['matchHeader']['team2']['name']:
                if include_game(scorecard['matchHeader']['matchDescription']):
                    match_info = j['children'][1]
                    yield scorecard,match_info
