from io import TextIOWrapper

class Logger:
    def __init__(self,filename='logs/logger.log'):
        self._log :TextIOWrapper = open(filename,'w')

    def Write(self, line):
        self._log.write(f'{line}')

    def HR(self, length=50, char='-'):
        """
        Draws a Horizonal line

        :param length: Length of Horizonal line. Default = 50
        :param char: Charater of Horizonal line. Default = - (hyphen)
        """
        self.WriteLn("-"*length)

    def WriteLn(self, line):
        self.Write(f'{line}\n')

    def close(self):
        print(f"Log made @: {self._log.name}")
        self._log.close()
