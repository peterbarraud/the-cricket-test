from enum import Enum

class OutType(Enum):
    NOTOUT = 0
    DIDNOTBAT = 1
    BOWLED = 2
    LBW = 3
    CAUGHT = 4
    CAUGHTBOWLED = 5
    STUMPED = 6
    RUNOUT = 7
    HITWICKET = 8
    HANDLED = 9
    OBSTRUCTION = 10
    ABSENTHURT = 11
    RETIREDHURT = 12
    RETIREDOUT = 13
    NONE = 14
