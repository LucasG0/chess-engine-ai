from engine.pieces.piece import Piece
from engine.position import Position

class King(Piece):
    def __init__(self, color):
        super(King,self).__init__("K",color,6)

    def get_pseudo_legal_pos(self, from_x, from_y, config):
        pos = []
        board = config.board
        x = 0
        y = 0
        for i in range(-1,2):
            for j in range(-1,2):
                x = from_x+i;
                y = from_y+j;
                if x >= 0 and x < 8 and y >= 0 and y < 8:
                    if (board[x][y].is_empty() or (board[x][y].piece.color != self.color)) and not(board[x][y].is_threat(not(self.color))):
                        pos.append(Position(x,y))
        self.addCastling(config,pos);
        return pos

    def get_threats_pos(self, from_x, from_y, config):
        pos = []
        board = config.board
        x = 0
        y = 0
        for i in range(-1,2):
            for j in range(-1,2):
                x = from_x+i;
                y = from_y+j;
                if x >= 0 and x < 8 and y >= 0 and y < 8:
                    pos.append(Position(x,y))
        return pos;

    # Add available castlings to the position list.
    def addCastling(self, config, pos):
        board = config.board
        player = config.player
        if player:
            if config.state.white_queen_castle:
                if board[1][7].is_empty() and board[2][7].is_empty() and board[3][7].is_empty():
                    if not(board[2][7].is_threat(0)) and not(board[3][7].is_threat(0)) and not(board[4][7].is_threat(0)):
                        pos.append(Position(2,7))
            if config.state.white_king_castle:
                if board[5][7].is_empty() and board[6][7].is_empty():
                    if not(board[4][7].is_threat(0)) and not(board[5][7].is_threat(0)) and not(board[6][7].is_threat(0)):
                        pos.append(Position(6,7))
        else:
            if config.state.black_queen_castle:
                if board[1][0].is_empty() and board[2][0].is_empty() and board[3][0].is_empty():
                    if not(board[2][0].is_threat(1)) and not(board[3][0].is_threat(1)) and not(board[4][0].is_threat(1)):
                        pos.append(Position(2,0))
            if config.state.black_king_castle:
                if board[5][0].is_empty() and board[6][0].is_empty():
                    if not(board[4][0].is_threat(1)) and not(board[5][0].is_threat(1)) and not(board[6][0].is_threat(1)):
                        pos.append(Position(6,0))
