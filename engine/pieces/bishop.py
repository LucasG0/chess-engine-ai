from chess.engine.pieces.piece import Piece
from chess.engine.position import Position

class Bishop(Piece):
    def __init__(self, color):
        super(Bishop,self).__init__("B",color,3)

    @staticmethod
    def pseudo_legal_pos(from_x, from_y, config, color):
        pos = []
        board = config.board
        i = 1
        for j in range(0,2):
            for k in range(0,2):
                i = 1
                x = from_x+i*j-i*(j==0)
                y = from_y+i*k-i*(k==0)
                while x >= 0 and x < 8 and  y >= 0 and y < 8 and board[x][y].is_empty():
                    pos.append(Position(x,y))
                    i += 1
                    x = from_x+i*j-i*(j==0)
                    y = from_y+i*k-i*(k==0)
                if x >= 0 and x < 8 and y >= 0 and y < 8 and not(board[x][y].is_empty()) and board[x][y].piece.color != color:
                    pos.append(Position(x,y))
        return pos

    @staticmethod
    def threats_pos(from_x, from_y, config, color):
            pos = []
            board = config.board
            i = 1
            for j in range(0,2):
                for k in range(0,2):
                    i = 1
                    x = from_x+i*j-i*(j==0)
                    y = from_y+i*k-i*(k==0)
                    while x >= 0 and x < 8 and  y >= 0 and y < 8 and board[x][y].is_empty():
                        pos.append(Position(x,y))
                        i += 1
                        x = from_x+i*j-i*(j==0)
                        y = from_y+i*k-i*(k==0)
                    if x >= 0 and x < 8 and y >= 0 and y < 8:
                        pos.append(Position(x,y))
            return pos

    def get_pseudo_legal_pos(self, from_x, from_y, config):
            return Bishop.pseudo_legal_pos(from_x,from_y,config,self.color)

    def get_threats_pos(self, from_x, from_y, config):
            return Bishop.threats_pos(from_x,from_y,config,self.color)
