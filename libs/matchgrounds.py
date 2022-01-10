from pickle import load, dump
from os.path import exists
from bs4 import BeautifulSoup as Bs
from bs4.element import Tag
from requests import get
from re import match as rematch, search as research
from libs.ground import Ground

class MatchGrounds:
    def __init__(self) -> None:
        self.__grounds : dict = None
        if exists("data.files/grounds.dict"):
            with open ("data.files/grounds.dict", 'rb') as f:
                self.__grounds : dict = load(f)
        else:
            self.__grounds = dict()

    def __del__(self) -> None:
        with open ("data.files/grounds.dict", 'wb') as f:
            dump(self.__grounds, f)

    def get_ground_by_id(self, ground_row : Tag):
        ground_link = ground_row.find('a').attrs['href']
        ground_id = research('\/([^\/]+?)\.html$',ground_link).group(1)
        if not self.__grounds.get(ground_id, False):
            soup = Bs(markup=get(url=ground_link).text, features='html.parser')
            m = rematch(pattern='^(.+?)\s*\|\s*(.+?)\s*\|', string=soup.title.get_text())
            self.__grounds[ground_id] =  Ground(m.group(1), m.group(2))
        return self.__grounds[ground_id]


