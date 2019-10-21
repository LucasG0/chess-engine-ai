from engine.position import Position
from engine.pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, color):
        super(Pawn,self).__init__("P",color,1)

    def get_pseudo_legal_pos(self, from_x, from_y, config):
        pos = []
        board = config.board
        if self.color:
            x = from_x
            y = from_y - 1
            if y >= 0 and board[x][y].is_empty():
                pos.append(Position(x,y))
            x = from_x
            y = from_y - 2
            if from_y == 6 and board[x][y].is_empty() and board[x][y+1].is_empty():
                pos.append(Position(x,y))
            x = from_x - 1
            y = from_y - 1
            if x >= 0 and y >= 0 and not(board[x][y].is_empty()) and board[x][y].piece.color != self.color:
                pos.append(Position(x,y))
            elif x >= 0 and y < 8 and from_y == 3 and config.state.ep_col == x:
                pos.append(Position(x,y))
            x = from_x + 1
            y = from_y - 1
            if x < 8 and y >= 0 and not(board[x][y].is_empty()) and board[x][y].piece.color != self.color:
                pos.append(Position(x,y))
            elif x >= 0 and y < 8 and from_y == 3 and config.state.ep_col == x:
                pos.append(Position(x,y))
        else:
            x = from_x
            y = from_y +  1
            if y >= 0 and board[x][y].is_empty():
                pos.append(Position(x,y))
            x = from_x
            y = from_y + 2
            if from_y == 1 and board[x][y].is_empty() and board[x][y-1].is_empty():
                pos.append(Position(x,y))
            x =from_x - 1
            y =from_y + 1
            if x >= 0 and y < 8 and not(board[x][y].is_empty()) and board[x][y].piece.color != self.color:
                pos.append(Position(x,y))
            elif x >= 0 and y < 8 and from_y == 4 and config.state.ep_col == x:
                pos.append(Position(x,y))
            x = from_x + 1
            y = from_y + 1
            if x < 8 and y < 8 and not(board[x][y].is_empty()) and board[x][y].piece.color != self.color:
                pos.append(Position(x,y))
            elif x >= 0 and y < 8 and from_y == 4 and config.state.ep_col == x:
                pos.append(Position(x,y))

        return pos


    def get_threats_pos(self, from_x, from_y, config):
        pos = []
        if self.color:
            x = from_x - 1
            y = from_y - 1
            if x >= 0 and x < 8 and y >= 0 and y < 8:
                pos.append(Position(x,y))
            x = from_x + 1
            y = from_y - 1
            if x >= 0 and x < 8 and y >= 0 and y < 8:
                pos.append(Position(x,y))
        else:
            x = from_x - 1
            y = from_y + 1
            if x >= 0 and x < 8 and y >= 0 and y < 8:
                pos.append(Position(x,y))
            x = from_x + 1
            y = from_y + 1
            if x >= 0 and x < 8 and y >= 0 and y < 8:
                pos.append(Position(x,y))

        return pos
