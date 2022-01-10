from enum import Enum
from re import match as rematch, IGNORECASE
class OutedHow(Enum):
    BOWLED = 1
    CAUGHT = 2
    LBW  = 3
    RUNOUT = 4
    NOTOUT = 5
    STUMPED = 6
    RETIREDOUT = 7
    HITWICKET = 8
    RETIREDHURT = 9
    HANDLEDTHEBALL = 10
    ABSENTHURT = 11
    ABSENTILL = 12
    RETIREDNOTOUT = 13
    RETIREDILL = 14
    OBSTRUCTINGTHEFIELD = 15
    

def get_outed_how(outedhowstr : str) -> OutedHow:
    '''Get how batter is outed. Bowled or Hit wicket or whatnot'''
    if rematch(pattern=r'\s*c\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.CAUGHT
    elif rematch(pattern=r'\s*b\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.BOWLED
    elif rematch(pattern=r'lbw+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.LBW
    elif rematch(pattern=r'run out', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RUNOUT
    elif rematch(pattern=r'not out', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.NOTOUT
    elif rematch(pattern=r'\s*st\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.STUMPED
    elif rematch(pattern=r'retired out', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RETIREDOUT      # TODO: What is "retired out"
    elif rematch(pattern=r'hit wicket', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.HITWICKET
    elif rematch(pattern=r'retired hurt', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RETIREDHURT
    elif rematch(pattern=r'handled the ball', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.HANDLEDTHEBALL
    elif rematch(pattern=r'absent hurt', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.ABSENTHURT
    elif rematch(pattern=r'absent ill', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.ABSENTILL
    elif rematch(pattern=r'retired not out', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RETIREDNOTOUT
    elif rematch(pattern=r'obstructing the field', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RETIREDILL
    elif rematch(pattern=r'retired ill', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RETIREDILL
    elif rematch(pattern=r'obstructing the field', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.OBSTRUCTINGTHEFIELD
    else:
        raise Exception(f'Unknowed outed method: {outedhowstr}')
