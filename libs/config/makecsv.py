# Saves each match to a .match file
# Data analysis / retrieval will happen through the .match files

from bs4 import BeautifulSoup as Bs
from zipfile import ZipFile
from bs4.element import ResultSet, Tag
from libs.config.info import CricketInfo
from os import walk as oswalk
from glob import glob
from os.path import exists
from re import match as rematch, search as research
from requests import get
from libs.config.ground import Ground
from pickle import load, dump

def match_file_generator():
    for (root,dirs,files) in oswalk(top='data.files', topdown=True):
        for file in files:
            if not str(file).endswith('dict') and not str(file).endswith('statuses'):
                yield f"{root}\{file}"


def __get_match_soup(match_file):
    unzipped = ZipFile(file=match_file,mode='r')
    return Bs(markup=unzipped.read('matcharchive'), features='html.parser')

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
            test_number = research(pattern=r'(\d+?)\s*$',string=row.find_all('td')[1].get_text()).group(1)
    return (test_number, ground.name, ground.country)


def makebattercsv(info : CricketInfo):
    grounds = dict()
    if exists("data.files/grounds.dict"):
        with open ("data.files/grounds.dict", 'rb') as f:
            grounds = load(f)
    for match_file in match_file_generator():
        soup : Bs = __get_match_soup(match_file=match_file)
        # each score has innings cards for the innings played and the last one for the match summary
        match_cards : ResultSet = soup.find_all(class_='match-scorecard-table')
        match_summary_card : Tag = match_cards.pop(-1)
        (test_number, ground, played_in_country) = __get_match_details(match_summary_card, grounds)
        innings_number : int = 0
        innings_card : Tag = None
        # since the last match card is the summary card, we're iterating till the second last
        for innings_number, innings_card in enumerate(match_cards):
            batter_score_tables = innings_card.find_all('table', class_='batsman')
            if len(batter_score_tables) == 1:
                # find the team playing
                batting_side : str = None
                m = rematch(pattern=r'^(.+?)\s+\d', string=innings_card.find('h5').get_text())
                batting_side : str = m.group(1)
                print(batting_side, innings_number)

    with open ("data.files/grounds.dict", 'wb') as f:
         dump(grounds, f)


        # if len(batter_score_tables) <= 4:
        #     for batter_score_table in batter_score_tables:
        #         for row in batter_score_table.tbody.find_all('tr'):
        #             if len(row.find_all('td')) == 8:
        #                 (name_cell, out_cell, runs_cell, balls_cells, mins_cells, fours_cell, sixes_cell, sr_cell) = row.find_all('td')
        #                 print(name_cell.get_text(), runs_cell.get_text())
        # else:
        #     raise Exception(f"Why are there so many batter tables - {len(batter_score_tables)}")


# For testing purposes only
def main():
    from libs.config.info import CricketInfo
    makebattercsv(CricketInfo())

if __name__ == '__main__':
    main()
    print('DONE')