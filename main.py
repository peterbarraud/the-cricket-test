from bs4 import BeautifulSoup
from requests import get
from sourcelinks import SourceLinks

def main():
    sourceLinks = SourceLinks()
    print(sourceLinks.YearList)
    soup = BeautifulSoup(get('https://www.cricbuzz.com/live-cricket-scorecard/8601/eng-vs-aus-only-test-australia-in-england-test-match-1880').text,'html.parser')
    with open('soup.txt', 'w') as f:
        f.write(soup.prettify())

if __name__ == "__main__":

    main()
    print('ALL DONE')