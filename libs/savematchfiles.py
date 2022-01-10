# Saves each match to a .match file
# Data analysis / retrieval will happen through the .match files

from requests import get
from bs4 import BeautifulSoup as Bs
from zipfile import ZipFile, ZIP_DEFLATED
from re import search as research
from pathlib import Path
from os import mkdir
from os.path import exists
from libs.config.info import CricketInfo


def save(info : CricketInfo, page):
    m = research(r'/([^/]+?)/([^/]+?)/[^/]+?$',page)
    filepath = m.group(1)
    filename = m.group(2)
    if not exists(f"data.files/match.files/{filepath}/{filename}.zip"):
        Path(f"data.files/match.files/{filepath}").mkdir(parents=True, exist_ok=True)
        zf = ZipFile(f"data.files/match.files/{filepath}/{filename}.zip", mode='w', compression=ZIP_DEFLATED)
        soup = Bs(markup=get(url=page).text, features='html.parser')
        zf.writestr('matcharchive', str(soup.find(class_=info.MainContentX)))
        zf.close()

# For testing purposes only
def main():
    from libs.config.info import CricketInfo
    save(None, 'https://stats.espncricinfo.com/series/england-tour-of-australia-1876-77-61716/australia-vs-england-2nd-test-62397/full-scorecard')

if __name__ == '__main__':
    try:
        main()
        print('DONE')
    except Exception as e:
        print(e)
