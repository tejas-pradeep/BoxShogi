import abc
can_promote = set(['r', 'g', 'n', 'p'])
class Piece(metaclass=abc.ABCMeta):
    """
    Class that represents a BoxShogi piece
    """

    def __init__(self, player_type, index):
        self.type = player_type
        self.x = index[0]
        self.y = index[1]
        self.moves = []
        self.isPromote = False
        pass

    def __repr__(self):
        return ""

    @abc.abstractmethod
    def updateMoves(self):
        pass

    @abc.abstractmethod
    def getMoves(self):
        pass

    @abc.abstractmethod
    def promote(self):
        pass

    def getPlayerType(self):
        return self.getPlayerType()

class Drive(Piece):

    def __init__(self, player_type, index):
        super(Drive, self).__init__(player_type, index)

    def updateMoves(self):
        moves = set()
        directions = [-1, 0, 1]
        for i in directions:
            for j in directions:
                if not(1 == 0 and j == 0):
                    moves.add((self.x + i, self.y + j))
        moves = list(moves)
        self.moves = moves

    def getMoves(self):
        return self.moves

    def promote(self):
        return False

class Notes(Piece):
    def __init__(self, player_type, index):
        super(Notes, self).__init__(player_type, index)

    def updateMoves(self):
        moves = set()
        for i in range(-5, 5):
            if i == 0:
                continue
            if 0 <= self.x + i < 5:
                moves.add((self.x + i, self.y))
            if 0 <= self.y + i < 5:
                moves.add((self.x, self.y + i))
        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if not (1 == 0 and j == 0):
                        moves.add((self.x + i, self.y + j))
        moves = list(moves)
        self.moves = moves

    def getMoves(self):
        return self.moves

    def promote(self):
        self.isPromote = True
        self.moves = self.getMoves()
        return True

class Governanace(Piece):
    def __init__(self, player_type, index):
        super(Governanace, self).__init__(player_type, index)

    def updateMoves(self):
        moves = set()
        j = 0
        for i in range(-2, 3):
            if i != 0 and 0 <= self.x + i < 5 and 0 <= self.y + i < 5:
                moves.add((self.x + i, self.y + i))
            j = -1 * i
            if i != 0 and 0 <= self.x + i < 5 and 0 <= self.y + j < 5:
                moves.add((self.x + i, self.y + j))
        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if not (1 == 0 and j == 0):
                        moves.add((self.x + i, self.y + j))
        self.moves = list(moves)

    def getMoves(self):
        return self.moves





