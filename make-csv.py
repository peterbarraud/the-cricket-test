# Saves each match to a .match file
# Data analysis / retrieval will happen through the .match files

from bs4 import BeautifulSoup as Bs
from zipfile import ZipFile
from bs4.element import ResultSet, Tag
from requests.models import ContentDecodingError
from libs.config.info import CricketInfo
from os import walk as oswalk
from glob import glob
from os.path import exists
from re import match as rematch, search as research, IGNORECASE
from requests import get
from libs.ground import Ground
from pickle import NONE, load, dump
from libs.outedhow import OutedHow, get_outed_how
from winsound import Beep
from timeit import timeit
from libs.savematchplayedlist import SaveMatchPlayedList

def match_file_generator():
    for (root,dirs,files) in oswalk(top='data.files', topdown=True):
        for file in files:
            if not str(file).endswith('dict') and not str(file).endswith('statuses'):
                yield f"{root}\{file}"


def __get_match_soup(match_file):
    unzipped = ZipFile(file=match_file,mode='r')
    return Bs(markup=unzipped.read('matcharchive'), features='html.parser')

def __save_match_file_for_checking(match_file : str):
    unzipped = ZipFile(file=match_file,mode='r')
    with open('testing.files/matcharchive.html', 'wb') as f:
        f.write(unzipped.read('matcharchive'))

def makebowlercsv(info : CricketInfo):
    pass

def __get_ground_name_and_country(groundTag : Tag, grounds : dict) -> Ground:
    ground_link = groundTag.find('a').attrs['href']
    ground_id = research('\/([^\/]+?)\.html$',ground_link).group(1)
    ground = grounds.get(ground_id, False)
    if not ground:
        soup = Bs(markup=get(url=ground_link).text, features='html.parser')
        m = rematch(pattern='^(.+?)\s*\|\s*(.+?)\s*\|', string=soup.title.get_text())
        grounds[ground_id] =  Ground(m.group(1), m.group(2))
    return grounds[ground_id]

# get the following
# Ground
# Played in country
# Match number
def __get_match_details(match_details_card : Tag, grounds) -> tuple:
    test_number : int = None
    ground_name : str = None
    ground_country : str = None
    for row_count, row in enumerate(match_details_card.find_all('tr')):
        if row_count == 0:
            ground : Ground = __get_ground_name_and_country(row, grounds)
        if row.td.get_text() == 'Match number':
            if research(pattern=r'(\d+?)\s*$',string=row.find_all('td')[1].get_text()) == None:
                # a freak case of the match being cancelled due to Covid
                # I believe these matches were not counted. But we'll see
                print(row.find_all('td')[1].get_text())
                test_number = research(pattern=r'(\d+?[a-z])\s*$',string=row.find_all('td')[1].get_text()).group(1)
            else:
                test_number = research(pattern=r'(\d+?)\s*$',string=row.find_all('td')[1].get_text()).group(1)
    return (test_number, ground.name, ground.country)


def makebattercsv():
    info : CricketInfo = CricketInfo()
    smpl = SaveMatchPlayedList()
    grounds = dict()
    if exists("data.files/grounds.dict"):
        with open ("data.files/grounds.dict", 'rb') as f:
            grounds = load(f)
    for match_file in match_file_generator():
        if smpl.has(match_file):
            continue
        if not match_file.endswith('south-africa-vs-england-4th-test-63863.zip'):
            continue
        print(match_file)
        soup : Bs = __get_match_soup(match_file=match_file)
        match_status = soup.find(class_='status-text')
        # if no "status" available for a match, implies it wasn't play
        if match_status:
            if rematch('Match (abandoned|cancelled) without a ball bowled', match_status.get_text()):
                continue
        else:   # not status-text was found so don't collect data
            continue
        # each score has innings cards for the innings played and the last one for the match summary
        match_cards : ResultSet = soup.find_all(class_=info.Scorecard)
        match_summary_card : Tag = match_cards.pop(-1)
        (test_number, ground, played_in_country) = __get_match_details(match_summary_card, grounds)
        innings_number : int = 0
        innings_card : Tag = None
        # since the last match card is the summary card, we're iterating till the second last
        for innings_number, innings_card in enumerate(match_cards):
            m = rematch(pattern=r'^(.+?)\s+\d', string=innings_card.find('h5').get_text())
            batting_side : str = m.group(1)
            batter_row : Tag = innings_card.find(class_=info.BatterTitleCell).parent
            (name, outedstr, runs, balls, mins, fours, sixes, _) = (x.get_text() for x in batter_row.find_all('td'))
            outed_how : OutedHow = get_outed_how(outedstr)
            smpl.append(match_file)
            # break
            # print(batting_side, innings_number,test_number, ground, played_in_country)


        # break

    with open ("data.files/grounds.dict", 'wb') as f:
         dump(grounds, f)

# For testing purposes only
def main():
    # __save_match_file_for_checking(r'data.files\aus-tour-of-sa-2017-18-1075977\south-africa-vs-australia-4th-test-1075985.zip')
    from libs.config.info import CricketInfo
    makebattercsv(CricketInfo())
    try:
        makebattercsv(CricketInfo())
    except Exception as e:
        print(e)

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
    # __save_match_file_for_checking('data.files\england-tour-of-south-africa-1999-00-61687\south-africa-vs-england-5th-test-63864.zip')
    t = timeit(stmt=makebattercsv, number=1)
    # test_match_files()
    # doneit(t)
