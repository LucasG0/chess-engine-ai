
class Square(object):
    def __init__(self, piece):
        self.white_threat = False
        self.black_threat = False
        self.piece = piece

    def reset_threat(self):
        self.white_threat = False
        self.black_threat = False

    def set_threat(self, color):
        if color:
            self.white_threat = True
        else:
            self.black_threat = True

    def is_threat(self,color):
        if color:
            return self.white_threat
        else:
            return self.black_threat

    def is_empty(self):
        return self.piece is None
