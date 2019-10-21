class Piece(object):
    def __init__(self, name, color, encode):
        self.color = color
        self.name = name
        self.encode = encode
        if not(color):
            self.encode = -self.encode

    def get_pseudo_legal_pos(self, from_x, from_y, config):
        raise NotImplementedError

    def get_threats_pos(self, from_x, from_y, config):
        raise NotImplementedError

    def can_pseudo_move(self, start, dest, config):
        from_x = start.x
        from_y = start.y
        xEnd = dest.x
        yEnd = dest.y
        positions = self.get_pseudo_legal_pos(from_x,from_y,config)
        for pos in positions:
            if pos.x == xEnd and pos.y == yEnd:
                return True
        return False
