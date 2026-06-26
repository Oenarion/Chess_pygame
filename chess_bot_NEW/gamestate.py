from enum import Enum

class GameState(Enum):
    ONGOING = 0
    CHECKMATE_WHITE_WINS = 1
    CHECKMATE_BLACK_WINS = 2
    DRAW_STALEMATE = 3
    DRAW_INSUFFICIENT = 4
    DRAW_FIFTY_MOVE = 5
    DRAW_THREEFOLD = 6
    PROMOTION = 7
    RESIGN_WHITE_WINS = 8   # black resigned
    RESIGN_BLACK_WINS = 9   # white resigned
    DRAW_AGREEMENT = 10
    TIMEOUT_WHITE_WINS = 11  # black ran out of time
    TIMEOUT_BLACK_WINS = 12  # white ran out of time