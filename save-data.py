from libs.config.info import CricketInfo
import libs.generators as generators
import libs.savematchfiles as savematchfiles
from timeit import timeit
from winsound import Beep
from libs.completedseries import CompletedSeriesList
from re import search as research

def savematchdatatofiles() -> None:
    info : CricketInfo = CricketInfo()
    completeSeries = CompletedSeriesList()
    for team_test_cricket_page in generators.team_test_page_generator(info):
        for series_results_page in generators.team_series_page_generator(info, team_test_cricket_page, completeSeries):
            print(series_results_page)
            for match_result_page in generators.scorecard_generator(info, series_results_page):
                savematchfiles.save(info, match_result_page)
            # set the series as over (probably)
            completeSeries.set_series_complete(series_results_page=series_results_page)

def main() -> None:
    savematchdatatofiles()

def doneit(time_taken_in_sec : float) -> None:
    time_to_run : float = 0.0
    unit_of_time = None
    for _ in range(2):
        Beep(500,100)
    if time_taken_in_sec/60 > 1:
        time_to_run = round(time_taken_in_sec/60, ndigits=2)
        unit_of_time = 'mins'
    else:
        time_to_run = round(time_taken_in_sec, 2)
        unit_of_time = 'secs'

    print(f'DONE in : {time_to_run} {unit_of_time}')

if __name__ == '__main__':
    t = timeit(stmt=main, number=1)
    doneit(t)
