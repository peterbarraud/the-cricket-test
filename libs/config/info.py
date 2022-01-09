import csv

class CricketInfo:
    def __init__(self) -> None:
        with open('libs/config/info.csv', 'r') as f:
            self.__items = dict()
            r = csv.DictReader(f, delimiter='|')
            for row in r:
                self.__items[row['page']] = row['url']
    
    @property
    def TeamsPage(self) -> str:
        return self.__items['teamspage']

    @property
    def TeamTestSeriesPageTemplate(self) -> str:
        return self.__items['teamtestseriespagetemplate']

    @property
    def TeamsGroup(self) -> str:
        return self.__items['teamsgroup']

    @property
    def HomeCenter(self) -> str:
        return self.__items['homecenter']

    @property
    def Scorecard(self) -> str:
        return self.__items['scorecard']

    @property
    def MainContentX(self) -> str:
        return self.__items['maincontentx']

    @property
    def AllInnings(self) -> str:
        return self.__items['allinnings']

    @property
    def InningsCard(self) -> str:
        return self.__items['inningscard']

    @property
    def BatterTitleCell(self) -> str:
        return self.__items['battertitlecell']

def main():
    i = CricketInfo()
    print(i.TeamsPage)
    print(i.TeamTestSeriesPageTemplate)

if __name__ == '__main__':
    main()
    