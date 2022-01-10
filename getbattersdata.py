# Saves each match to a .match file
# Data analysis / retrieval will happen through the .match files

from bs4 import BeautifulSoup as Bs
from zipfile import ZipFile
from bs4.element import ResultSet, Tag
from libs.config.info import CricketInfo
from re import L, match as rematch, search as research
from libs.ground import Ground
from libs.outedhow import OutedHow, get_outed_how
from winsound import Beep
from timeit import timeit
from libs.generators import match_file_generator
from libs.matchgrounds import MatchGrounds
from libs.savecsv import SaveCsv

def __save_match_file_for_checking(match_file : str):
    unzipped = ZipFile(file=match_file,mode='r')
    with open('testing.files/matcharchive.html', 'wb') as f:
        f.write(unzipped.read('matcharchive'))

def makebowlercsv(info : CricketInfo):
    pass

# get the following
# Ground
# Played in country
# Match number
def __get_match_details(match_details_card : Tag, grounds: MatchGrounds) -> tuple:
    '''From the match card, get: Test match number, ground name and played in country'''
    test_number : int = None
    for row_count, row in enumerate(match_details_card.find_all('tr')):
        if row_count == 0:
            ground : Ground = grounds.get_ground_by_id(row)
        if row.td.get_text() == 'Match number':
            if research(pattern=r'(\d+?)\s*$',string=row.find_all('td')[1].get_text()) == None:
                test_number = research(pattern=r'(\d+?[a-z])\s*$',string=row.find_all('td')[1].get_text()).group(1)
            else:
                test_number = research(pattern=r'(\d+?)\s*$',string=row.find_all('td')[1].get_text()).group(1)
    return (test_number, ground.name, ground.country)


def __get_cleaned_name(namestr : str) -> tuple:
    '''Names often have the captain or wicketkeeper moniker at the end'''
    is_cap : bool = False
    name : str = namestr
    is_wk : bool = False
    if namestr.strip().endswith('(c)'):
        is_cap = True
        name = namestr.strip().rstrip('(c)')
    elif namestr.strip().endswith('†'):
        is_wk = True
        name = namestr.strip().rstrip('†')
    return (name.strip(), is_cap, is_wk)
    
# Use match status to find out if we need to get the match data
def __is_match_played(soup : Bs) -> bool:
    '''Check if match was played. Maybe abandoned or cancelled or something'''
    match_status = soup.find(class_='status-text')
    # if no "status" available for a match, implies it wasn't play
    if match_status:
        if rematch('Match (abandoned|cancelled) without a ball bowled', match_status.get_text()):
            return False
    else:   # not status-text was found so don't collect data
        return False
    return True

def __logwrite(line, log):
    log.write(f'{line}\n')

def makebattercsv():
    info : CricketInfo = CricketInfo()
    grounds = MatchGrounds()
    savecsv = SaveCsv()
    for match_file in match_file_generator():
        print(match_file)
        unzipped = ZipFile(file=match_file,mode='r')
        soup : Bs = Bs(markup=unzipped.read('matcharchive'), features='html.parser')
        if not __is_match_played(soup):
            continue
        # each score has innings cards for the innings played and the last one for the match summary
        match_cards : ResultSet = soup.find_all(class_=info.Scorecard)
        match_summary_card : Tag = match_cards.pop(-1)
        (test_number, ground, played_in_country) = __get_match_details(match_summary_card, grounds)        
        innings_card : Tag = None
        for i, innings_card in enumerate(match_cards):
            innings_number : int = i + 1
            m = rematch(pattern=r'^(.+?)\s+\d', string=innings_card.find('h5').get_text())
            batting_side : str = m.group(1)
            batter_title_rows : Tag = innings_card.find_all(class_=info.BatterTitleCell)
            for batter_title_row in batter_title_rows:
                batter_row = batter_title_row.parent
                # in later times, they've added a cell for the video of how batter outed. So, it's previously 8 now 9 cells
                batter_cells = batter_row.find_all('td')
                if len(batter_cells) == 8:
                    (namestr, outedstr, runs, balls, mins, fours, sixes, _) = (x.get_text() for x in batter_row.find_all('td'))
                elif len(batter_cells) == 9:
                    (namestr, outedstr, runs, balls, mins, fours, sixes, _, _) = (x.get_text() for x in batter_row.find_all('td'))
                outed_how : OutedHow = get_outed_how(outedstr)
                (name, is_cap, is_wk) = __get_cleaned_name(namestr=namestr)
                savecsv.writerow(name=name,playedin=played_in_country,side=batting_side,
                                    captain=is_cap, outedhow=outed_how.value, runs=runs,
                                    wicketkeeper=is_wk,innings=innings_number,testnumber=test_number)

def doneit(time_taken_in_sec : float) -> None:
    time_to_run : float = 0.0
    unit_of_time = None
    for _ in range(2):
        Beep(2000,100)
    if time_taken_in_sec/60 > 1:
        time_to_run = round(time_taken_in_sec/60, ndigits=2)
        unit_of_time = 'mins'
    else:
        time_to_run = round(time_taken_in_sec, 2)
        unit_of_time = 'secs'

    print(f'DONE in : {time_to_run} {unit_of_time}')

if __name__ == '__main__':
    t = timeit(stmt=makebattercsv, number=1)
    doneit(t)
    # __save_match_file_for_checking(r'data.files/match.files\india-in-australia-2020-21-1223867\australia-vs-india-1st-test-1223869.zip')
