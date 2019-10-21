# Represents the state of a chess board.
class State(object):
    def __init__(self, state=None):
        if state is None:
            self.black_king_castle = True
            self.black_queen_castle = True
            self.white_king_castle = True
            self.white_queen_castle = True
            self.ep_col = -1
            self.fifty_moves_rules = 0
            self.white_history = [1,2,3,4,5]
            self.black_history = [1,2,3,4,5]
        else:
            self.black_king_castle = state.black_king_castle
            self.black_queen_castle = state.black_queen_castle
            self.white_king_castle = state.white_king_castle
            self.white_queen_castle = state.white_queen_castle
            self.ep_col = state.ep_col
            self.fifty_moves_rules = state.fifty_moves_rules
            self.white_history = state.white_history.copy()
            self.black_history = state.black_history.copy()
