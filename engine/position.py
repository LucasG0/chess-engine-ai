
class Position(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return Position.char(self.x) + str(8-self.y)

    @staticmethod
    def char(value):
        value += 1
        if value == 1:
            return 'a'
        elif value == 2:
            return 'b'
        elif value == 3:
            return 'c'
        elif value == 4:
            return 'd'
        elif value == 5:
            return 'e'
        elif value == 6:
            return 'f'
        elif value == 7:
            return 'g'
        elif value == 8:
            return 'h'
        else:
            raise TypeError
