from engine.pieces.piece import Piece
from engine.pieces.rook import Rook
from engine.pieces.bishop import Bishop
from engine.position import Position

class Queen(Piece):
    def __init__(self, color):
        super(Queen,self).__init__("Q",color,5)

    def get_pseudo_legal_pos(self, from_x, from_y, config):
        pos = []
        bishop_pos = Bishop.pseudo_legal_pos(from_x,from_y,config,self.color)
        rook_pos = Rook.pseudo_legal_pos(from_x,from_y,config,self.color)
        for b_pos in bishop_pos:
            pos.append(b_pos)
        for r_pos in rook_pos:
            pos.append(r_pos)
        return pos

    def get_threats_pos(self, from_x, from_y, config):
        pos = []
        bishop_pos = Bishop.threats_pos(from_x,from_y,config,self.color)
        rook_pos = Rook.threats_pos(from_x,from_y,config,self.color)
        for b_pos in bishop_pos:
            pos.append(b_pos)
        for r_pos in rook_pos:
            pos.append(r_pos)
        return pos
