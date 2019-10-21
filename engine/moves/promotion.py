from chess.engine.moves.standard_move import StandardMove
from chess.engine.pieces.queen import Queen
from chess.engine.state import State

# Represents a promotion move. Promoted pawn is auto promotion as a queen.
class Promotion(StandardMove):
    def __init__(self, start, dest, moving_piece):
        super(Promotion,self).__init__(start,dest,moving_piece)
        self.promoted = None
        self.new_queen = None

    def apply(self, config):
        self.apply_standard(config)
        board = config.board
        dest_square = board[self.dest.x][self.dest.y]
        self.promoted = dest_square.piece
        if config.player:
            self.new_queen = Queen(True)
        else:
            self.new_queen = Queen(False)
        dest_square.piece = self.new_queen

    def cancel(self, config):
        board = config.board
        board[self.dest.x][self.dest.y].piece = self.promoted
        self.cancel_standard(config)
