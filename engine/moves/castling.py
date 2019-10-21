from engine.moves.standard_move import StandardMove
from engine.state import State
from engine.pieces.piece import Piece
from engine.position import Position

# Represents either a king or queen castling, defined by a standard move (king) and an added rook move.
class Castling(StandardMove):
    def __init__(self, start, dest, moving_piece, rook):
        super(Castling,self).__init__(start,dest,moving_piece)
        if dest.x == 2:
            self.rook_move = StandardMove(Position(0,dest.y),Position(3,dest.y),rook)
        elif dest.x == 6:
            self.rook_move = StandardMove(Position(7,dest.y),Position(5,dest.y),rook)

    def apply(self, config):
        self.apply_standard(config)
        self.rook_move.apply_standard(config)

    def cancel(self, config):
        self.cancel_standard(config)
        self.rook_move.cancel_standard(config)
