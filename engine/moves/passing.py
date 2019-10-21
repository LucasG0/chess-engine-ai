from engine.moves.standard_move import StandardMove
from engine.pieces.pawn import Pawn
from engine.state import State

# Represents a "En passant" move.
class Passing(StandardMove):
    def __init__(self, start, dest, moving_piece):
        super(Passing,self).__init__(start,dest,moving_piece)
        self.deleted_pawn = None

    def apply(self, config):
        self.apply_standard(config)
        board = config.board
        square = None
        if config.player:
            square = board[self.dest.x][3]
        else:
            square = board[self.dest.x][4]
        self.deleted_pawn = square.piece
        square.piece = None

    def cancel(self, config):
        board = config.board
        if config.player:
            board[self.dest.x][3].piece = self.deleted_pawn
        else:
            board[self.dest.x][4].piece = self.deleted_pawn
        self.deleted_pawn = None
        self.cancel_standard(config)
