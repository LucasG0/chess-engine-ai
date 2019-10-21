from engine.pieces.piece import Piece
from engine.position import Position

class Rook(Piece):
    def __init__(self,color):
        super(Rook,self).__init__("R",color,4)

    @staticmethod
    def pseudo_legal_pos(from_x, from_y, config, color):
            pos = []
            board = config.board
            i = 1
            while from_x+i < 8 and board[from_x+i][from_y].is_empty():
                pos.append(Position(from_x+i,from_y))
                i += 1
            if from_x+i < 8 and not(board[from_x+i][from_y].is_empty()) and board[from_x+i][from_y].piece.color != color:
                pos.append(Position(from_x+i,from_y))
            i = 1
            while from_x-i >= 0 and board[from_x-i][from_y].is_empty():
                pos.append(Position(from_x-i,from_y))
                i += 1
            if from_x-i >= 0 and not(board[from_x-i][from_y].is_empty()) and board[from_x-i][from_y].piece.color != color:
                pos.append(Position(from_x-i,from_y))
            i = 1
            while from_y+i < 8 and board[from_x][from_y+i].is_empty():
                pos.append(Position(from_x,from_y+i))
                i += 1
            if from_y+i < 8 and not(board[from_x][from_y+i].is_empty()) and board[from_x][from_y+i].piece.color != color:
                pos.append(Position(from_x,from_y+i))
            i = 1
            while from_y-i >= 0 and board[from_x][from_y-i].is_empty():
                pos.append(Position(from_x,from_y-i))
                i += 1
            if from_y-i >= 0 and not(board[from_x][from_y-i].is_empty()) and board[from_x][from_y-i].piece.color != color:
                pos.append(Position(from_x,from_y-i))

            return pos

    @staticmethod
    def threats_pos(from_x, from_y, config, color):
        pos = []
        board = config.board
        i = 1
        while from_x+i < 8 and board[from_x+i][from_y].is_empty():
            pos.append(Position(from_x+i,from_y))
            i += 1
        if from_x+i < 8:
            pos.append(Position(from_x+i,from_y))
        i = 1
        while from_x-i >= 0 and board[from_x-i][from_y].is_empty():
            pos.append(Position(from_x-i,from_y))
            i += 1
        if from_x-i >= 0:
            pos.append(Position(from_x-i,from_y))
        i = 1
        while from_y+i < 8 and board[from_x][from_y+i].is_empty():
            pos.append(Position(from_x,from_y+i))
            i += 1
        if from_y+i < 8:
            pos.append(Position(from_x,from_y+i))
        i = 1
        while from_y-i >= 0 and board[from_x][from_y-i].is_empty():
            pos.append(Position(from_x,from_y-i))
            i += 1
        if from_y-i >= 0:
            pos.append(Position(from_x,from_y-i))

        return pos

    def get_pseudo_legal_pos(self, from_x, from_y, config):
        return Rook.pseudo_legal_pos(from_x,from_y,config,self.color)

    def get_threats_pos(self, from_x, from_y, config):
        return Rook.threats_pos(from_x,from_y,config,self.color)
