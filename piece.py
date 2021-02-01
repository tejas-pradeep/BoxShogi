import abc
can_promote = set(['r', 'g', 'n', 'p'])
class Piece(metaclass=abc.ABCMeta):
    """
    Class that represents a BoxShogi piece
    """

    def __init__(self, player_type, index, name):
        self.type = player_type
        self.col = index[0]
        self.row = index[1]
        self.name = name
        self.moves = []
        self.isPromote = False
        self.updateMoves()
        pass

    def __repr__(self):
        return ""

    @abc.abstractmethod
    def updateMoves(self):
        pass

    @abc.abstractmethod
    def getMoves(self):
        pass

    def promote(self):
        pass

    def getPlayerType(self):
        return self.type

    def toString(self):
        if self.type.islower():
            return self.name.lower()
        else:
            return self.name.upper()

    def getLocation(self):
        return self.col, self.row

class Drive(Piece):

    def __init__(self, player_type, index):
        super(Drive, self).__init__(player_type, index, 'd')

    def updateMoves(self, check_moves=None):
        moves = set()
        directions = [-1, 0, 1]
        for i in directions:
            for j in directions:
                if not(i == 0 and j == 0) and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                    moves.add((self.col + i, self.row + j))
        moves = list(moves)
        self.moves = moves

    def getMoves(self):
        return self.moves

    def promote(self):
        return False

class Notes(Piece):
    #need to account for pieces in the way
    def __init__(self, player_type, index):
        super(Notes, self).__init__(player_type, index, 'n')

    def updateMoves(self, blocked_path=None):
        """
        Rook moves in four directions, to account for blockages I am using 4 loops to add moves in each direction
        :param blocked_path:
        :return:
        """
        moves = set()
        #vertically positive moves
        for i in range(5):
            if self.row + i > 4:
                break
            if ((self.col, self.row + i) in)

        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if not (i == 0 and j == 0) and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                        moves.add((self.col + i, self.row + j))
        moves = list(moves)
        self.moves = moves

    def getMoves(self):
        return self.moves

    def promote(self):
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True

class Governanace(Piece):
    def __init__(self, player_type, index):
        super(Governanace, self).__init__(player_type, index, 'g')

    def updateMoves(self, blocked_path=None):
        moves = set()
        j = 0
        for i in range(-2, 3):
            if i != 0 and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                moves.add((self.col + i, self.row + i))
            j = -1 * i
            if i != 0 and 0 <= self.row + i < 5 and 0 <= self.col + j < 5:
                moves.add((self.col + i, self.row + j))
        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if not (i == 0 and j == 0) and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                        moves.add((self.col + i, self.row + j))
        self.moves = list(moves)

    def getMoves(self):
        return self.moves

    def promote(self):
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True


class Shield(Piece):
    def __init__(self, player_type, index):
        super(Shield, self).__init__(player_type, index, 's')

    def updateMoves(self):
        moves = set()
        directions = [-1, 0, 1]
        for i in directions:
            for j in directions:
                if i != 0 or j != 0 and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                    if (i, j) != (-1, -1) and (i, j) != (1, -1):
                        moves.add((self.col + i, self.row + j))
        self.moves = list(moves)
    def getMoves(self):
        return self.moves

    def promote(self):
        return False

class Relay(Piece):
    def __init__(self, player_type, index):
        super(Relay, self).__init__(player_type, index, 'r')

    def updateMoves(self):
        moves = set()
        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if i != 0 or j != 0 and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                        if (i, j) != (-1, -1) and (i, j) != (1, -1):
                            moves.add((self.col + i, self.row + j))
        else:
            banned_list = [(-1, 0), (1, 0), (0, -1)]
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if i != 0 or j != 0 and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                        if (i, j) not in banned_list:
                            moves.add((self.col + i, self.row + j))
        self.moves = list(moves)

    def getMoves(self):
        return self.moves

    def promote(self):
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True

class Preview(Piece):
    def __init__(self, player_type, index):
        super(Preview, self).__init__(player_type, index, 'p')
    def updateMoves(self):
        if self.isPromote:
            moves = set()
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if i != 0 or j != 0 and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                        if (i, j) != (-1, -1) and (i, j) != (1, -1):
                            moves.add((self.col + i, self.row + j))
            self.moves = list(moves)
        else:
            if self.row + 1 < 5:
                self.moves = [(self.col, self.row + 1)]
    def getMoves(self):
        return self.moves
    def promote(self):
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True










