from csv import reader,DictWriter
from json import dumps,loads
from bs4 import BeautifulSoup as BS4
from requests import get
from re import compile,search,sub as resub,MULTILINE
from pathlib import Path
from pickle import load as loadp,dump as dumpp

from libs.logger import Logger
from libs.dataclasses import GameInfo


def get_home_team_exceptions():
    """
    Some teams don't have a home (not exactly, but...).
    Like Afg doesn't host matches. Some other countries. So, we're going to keep a list of the alternate homes per game
    One exception - World Test Championship finals
    """
    home_team_exceptions : dict = dict()
    with open('data/home-team-exceptions.csv') as f:
        for row in reader(f):
            home_team_exceptions[int(row[0])] = int(row[1])
        return home_team_exceptions


def __get_team_captains(team_info : list,teamsd : dict):
    team1captain : int = 0
    team2captain : int = 0
    for team in team_info:
        team_name = team[3]['children'][0][3]['children'][0]
        players = team[3]['children'][1][3]['children'][3]['children'][1][3]['children'][0]
        for player in players:
            if '(c)' in player[3]['children'][1]:
                if teamsd[team_name] == 'team1':
                    team1captain = player[2]
                    continue
                elif teamsd[team_name] == 'team2':
                    team2captain = player[2]
                    continue
    return team1captain,team2captain

def __get_series_soup(game_id,config):
    series_soup = None
    soup_file_path = Path(f"data/series.soups/{game_id}.soup")
    if soup_file_path.exists():
        with open(soup_file_path,'rb') as f:
            series_soup : BS4 = loadp(f)
    else:
        match_facts_url : str = f"{config['server']}/cricket-match-facts/{game_id}"
        mf_soup = BS4(get(match_facts_url).text,'html.parser')
        anchors = mf_soup.find_all('a',{'title':'INFO'})
        if len(anchors) == 1:
            series_href = anchors[0].parent.find('a',{'href':compile('^/cricket-series.+?matches$')}).attrs['href']
            series_href = f"{config['server']}{series_href}"
        else:
            raise Exception("too many INFO anchors")
        if not series_href.startswith(config['server']):
            series_href = f"{config['server']}{series_href}"
        series_soup = BS4(get(series_href).text,'html.parser')
        # finally save this to a soup file (so next time we don't have to do that whole everything)
        with open(soup_file_path,'wb') as f:
            dumpp(series_soup,f)
    return series_soup

def __get_game_dates(game_id,match_description,config):
    series_soup = __get_series_soup(game_id,config)
    for script_tag in series_soup.find_all('script'):
        script_tag_text : str = script_tag.text
        if script_tag_text.startswith('self.__next_f.push') and match_description in script_tag_text:
            g = search(r'^.+?(\{.+?\})\]\\n\"\]\)',script_tag_text)
            if g:
                mains = g.groups()[0].replace("\\","")
                # '"matchDesc":"1st Test","matchFormat":"TEST","startDate":"1726718400000","endDate":"1727064000000"'
                re_pattern = rf'"matchDesc":"{match_description.replace('(','\(').replace(')','\)')}","matchFormat":"TEST","startDate":"(-?\d+?)","endDate":"(-?\d+?)"'
                g1 = search(re_pattern,mains,MULTILINE)
                if g1 and len(g1.groups()) == 2:
                    # we are going to remove the millseconds last 000
                    start_date,end_date = [int(x) for x in g1.groups()]
                    if start_date % 1000 == 0:
                        start_date = int(start_date/1000)
                    else:
                        raise Exception("Start date isn't divisible by 1000")
                    if end_date % 1000 == 0:
                        end_date = int(end_date/1000)
                    else:
                        raise Exception("End date isn't divisible by 1000")
                    return start_date,end_date
    raise Exception("Error at end of __get_game_dates")


def get_game_info(game_header,team_info,config:dict):
    teamd : dict = dict()
    home_team_exceptions : dict = get_home_team_exceptions()
    # tossWinner = game_header['tossResults'].get('tossWinnerId',0) # seems that for many games, we haven't got any toss details
    # descisionToBat = game_header['tossResults'].get('decision',None) == 'Batting' # seems that for many games, we haven't got any toss details
    game_info = GameInfo()
    game_info.Id = game_header['matchId']
    game_info.Series = game_header['seriesId']
    game_info.Start,game_info.End = __get_game_dates(game_header['matchId'],game_header['matchDescription'],config)    
    game_info.TossWinner = game_header['tossResults'].get('tossWinnerId',0)
    game_info.DescisionToBat = game_header['tossResults'].get('decision',None) == 'Batting'
    game_info.Team1 = game_header['team1']['id']
    game_info.Team2 = game_header['team2']['id']
    teamd[game_header['team1']['name']] = 'team1'
    teamd[game_header['team2']['name']] = 'team2'
    game_info.Team1Captain,game_info.Team2Captain = __get_team_captains(team_info,teamd)
    if game_header['team1']['name'] == game_header['venue']['country']:
        game_info.HomeTeam = game_header['team1']['id']
    elif game_header['team2']['name'] == game_header['venue']['country']:
        game_info.HomeTeam = game_header['team2']['id']
    else:
        game_info.HomeTeam = home_team_exceptions[game_info.Id]
    game_info.Venue = game_header['venue']['id']

    if game_header['result'] and game_header['result'].get('winningteamId',False):
        game_info.Winner = game_header['result']['winningteamId']
        game_info.Margin = game_header['result']['winningMargin']
        game_info.IsWinByRuns = game_header['result']['winByRuns']
        game_info.IsInningsWin = game_header['result']['winByInnings']
    return game_info

