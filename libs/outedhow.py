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

def get_outed_how(outedhowstr : str) -> OutedHow:
    if rematch(pattern=r'\s*c\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.CAUGHT
    elif rematch(pattern=r'\s*b\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.BOWLED
    elif rematch(pattern=r'\s*lbw\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.LBW
    elif rematch(pattern=r'\s*lbw\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.LBW
    elif rematch(pattern=r'\s*run out\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RUNOUT
    elif rematch(pattern=r'\s*not out\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.NOTOUT
    elif rematch(pattern=r'\s*st\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.STUMPED
    elif rematch(pattern=r'\s*retired out\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RETIREDOUT      # TODO: What is "retired out"
    elif rematch(pattern=r'\s*hit wicket\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.HITWICKET
    elif rematch(pattern=r'\s*retired hurt\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.RETIREDHURT
    elif rematch(pattern=r'\s*handled the ball\s+', string=outedhowstr, flags=IGNORECASE):
        return OutedHow.HANDLEDTHEBALL
        
    else:
        raise Exception(f'Unknowed outed method: {outedhowstr}')
