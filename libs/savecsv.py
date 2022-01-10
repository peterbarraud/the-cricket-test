from csv import DictWriter
from dataclasses import dataclass

class SaveCsv:
    def __init__(self):
        self.__writer : DictWriter = None
        self.__csvfile = open('data.files/batters.csv', 'w', newline='')
        fieldnames = ['name', 'outedhow','runs', 'captain','wicketkeeper','side','testnumber','playedin','innings']
        self.__writer = DictWriter(self.__csvfile, fieldnames=fieldnames)      
        self.__writer.writeheader()  

    def __del__(self) -> None:
        self.__csvfile.close()

    def writerow(self, **kwargs):
        self.__writer.writerow(kwargs)



