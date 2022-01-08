from requests import get
from bs4 import BeautifulSoup as Bs
from re import search as research
from os import walk as oswalk

from libs.config.info import CricketInfo
from libs.completedseries import CompletedSeriesList


def team_test_page_generator(info):
    soup = Bs(markup=get(url=info.TeamsPage).text, features='html.parser')
    rec_by_team = soup.find(id=info.TeamsGroup)
    items = rec_by_team.find_all('a')
    for item in items:
        m = research('id=(\d+)?',item.attrs['href'])
        yield info.TeamTestSeriesPageTemplate.replace('<id>', m.groups()[0])

def get_series_results_page_url(page):
    r = get(page)
    return r.url.replace('match-schedule-fixtures','match-results')

def team_series_page_generator(info, page, completedseries : CompletedSeriesList):
    if page == 'https://stats.espncricinfo.com/ci/engine/records/team/series_results.html?class=1;id=46;type=team':
        print(page)
    soup = Bs(markup=get(url=page).text, features='html.parser')
    country : str = research('^(.+?)\s+Cricket',soup.title.get_text()).group(1)
    print(f"Getting for: {country}")
    series_body = soup.table.tbody
    if series_body:
        for row in series_body.find_all('tr'):
            series_page = row.a.attrs["href"]
            series_id : int = int(research('\/(\d+?).html',series_page).group(1))
            if completedseries.is_series_complete(series_id=series_id):
                continue
            else:
                yield get_series_results_page_url(f'{info.HomeCenter}{series_page}')

def scorecard_generator(info : CricketInfo, page : str):
    soup = Bs(markup=get(url=page).text, features='html.parser')
    for scorecard in soup.find_all('a', {'data-hover':'Scorecard'}):
        yield f'{info.HomeCenter}{scorecard.attrs["href"]}'

def series_id_generator():
    for (root,dirs,files) in oswalk(f'data.files', topdown=True):
        for dir in dirs:
            yield dir

def main():
    print('This is a PURE CLASS. You should call this from some main function')

if __name__ == '__main__':
    main()
