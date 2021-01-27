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
