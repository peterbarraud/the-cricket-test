from pickle import load, dump
from os.path import exists
from bs4 import BeautifulSoup as Bs
from requests import get
from re import search as research

class CompletedSeriesList:
    def __init__(self) -> None:
        self.__completed_series = list()
        if exists('data.files/series.statuses'):
            with open('data.files/series.statuses', 'rb') as f:
                self.__completed_series = load(f)

    def __del__(self) -> None:
        with open('data.files/series.statuses', 'wb') as f:
            dump(self.__completed_series, f)

    def set_series_complete(self, series_results_page : str) -> None:
        series_fixtures_page = series_results_page.replace('match-results','match-schedule-fixtures')
        series_id : int = int(research('\-(\d+?)\/match-schedule-fixtures$',series_fixtures_page).group(1))
        if not self.is_series_complete(series_id=series_id):
            soup = Bs(markup=get(series_fixtures_page).text, features='html.parser')
            if len(soup.find_all(class_='no-matches-container')) == 1:
                self.__completed_series.append(series_id)


    # True: If the series is complete and we've recorded it
    # False: Else
    def is_series_complete(self, series_id : int) -> bool:
        return series_id in self.__completed_series
