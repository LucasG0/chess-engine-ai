from chess.engine.pieces.piece import Piece
from chess.engine.position import Position

class Knight(Piece):
    def __init__(self, color):
        super(Knight,self).__init__("N",color,2)

    def get_pseudo_legal_pos(self, from_x, from_y, config):
        pos = []
        board = config.board
        x = 0
        y = 0
        for i in range(-2,3):
            for j in range(-2,3):
                x = from_x+i;
                y = from_y+j;
                if x >= 0 and x < 8 and y >= 0 and y < 8 and abs(i)+abs(j)== 3:
                    if board[x][y].is_empty() or board[x][y].piece.color != self.color:
                        pos.append(Position(x,y))
        return pos


    def get_threats_pos(self, from_x, from_y, config):
        pos = []
        x = 0
        y = 0
        for i in range(-2,3):
            for j in range(-2,3):
                x = from_x+i;
                y = from_y+j;
                if x >= 0 and x < 8 and y >= 0 and y < 8 and abs(i)+abs(j)== 3:
                    pos.append(Position(x,y))
        return pos
