from pickle import dump, load
from os.path import exists

class SaveMatchPlayedList:
    def __init__(self) -> None:
        self.__list : list = None
        if exists('testing.files/played.list'):
            with open('testing.files/played.list', 'rb') as f:
                self.__list = load(f)
        else:
            self.__list = list()
    
    def __del__(self) -> None:
        with open('testing.files/played.list', 'wb') as f:
            dump(self.__list, f)
    
    def append(self, match_file : str) -> None:
        self.__list.append(match_file)

    def has(self, match_file : str) -> bool:
        return match_file in self.__list