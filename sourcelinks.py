from json import load
class SourceLinks:
    def __init__(self):
        with open('links.json') as f:
            self.__json = load(f)
    
    @property
    def YearList(self):
        return self.__json['year-list']
