import abc
can_promote = set(['r', 'g', 'n', 'p'])
class Piece(metaclass=abc.ABCMeta):
    """
    Class that represents a BoxShogi piece
    """

    def __init__(self, type, index):
        self.type = type
        self.x = index[0]
        self.y = index[1]
        pass

    def __repr__(self):
        return ""

    @abc.abstractmethod
    def getMoves(self):
        pass

    @abc.abstractmethod
    def promote(self):
        pass

class Drive(Piece):

    def __init__(self, type, index):
        super(Drive, self).__init__(type, index)

    def getMoves(self):
        moves = set()
        directions = [-1, 0, 1]
        for i in directions:
            for j in directions:
                if not(1 == 0 and j == 0):
                    moves.add((self.x + i, self.y + j))
        return list(moves)

    def promote(self):
        return False
