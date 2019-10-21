from chess.engine.state import State
from chess.engine.utils import *

# Represents a chess move, defined by a start/destination square, and a piece.
class StandardMove(object):
    def __init__(self,start,dest,moving_piece):
        self.start = start
        self.dest = dest
        self.moving_piece = moving_piece
        self.deleted_piece = None
        self.previous_state = None
        self.previous_threats = None

    def __str__(self):
        return str(self.start) + "" + str(self.dest)

    def is_legal(self,config):
        config.apply_move(self,False)
        legal = not(config.is_check(config.player))
        config.cancel_move(self)
        return legal

    # This method can be implemented in sub-classes.
    def apply(self,config):
        self.apply_standard(config)

    def cancel(self,config):
        self.cancel_standard(config)


    def apply_standard(self,config):
        board = config.board
        start = board[self.start.x][self.start.y]
        dest = board[self.dest.x][self.dest.y]
        if dest.piece != None:
            self.deleted_piece = dest.piece
        dest.piece = self.moving_piece
        start.piece = None

    def cancel_standard(self,config):
        board = config.board
        start = board[self.start.x][self.start.y]
        dest = board[self.dest.x][self.dest.y]
        start.piece = self.moving_piece
        dest.piece = self.deleted_piece

    # Convert a move to an int representation.
    def number(self,revert):
        if revert:
            start = (7-self.start.y) * 8 + (7-self.start.x)
            dest = (7-self.dest.y) * 8 + (7-self.dest.x)
        else:
            start = self.start.y * 8 + self.start.x
            dest = self.dest.y * 8 + self.dest.x
        return start * 63 + dest
