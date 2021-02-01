import abc
#Check bounds is a method that checks if a given index is in bounds of the board
from utils import checkBounds

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
    def updateLocation(self, new_location):
        self.col = new_location[0]
        self.row = new_location[1]


class Drive(Piece):

    def __init__(self, player_type, index):
        super(Drive, self).__init__(player_type, index, 'd')

    def updateMoves(self, check_moves=list()):
        moves = set()
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
        return False


class Notes(Piece):
    # need to account for pieces in the way
    def __init__(self, player_type, index):
        super(Notes, self).__init__(player_type, index, 'n')

    def updateMoves(self, blocked_path=list()):
        """
        Rook moves in four directions, to account for blockages I am using 4 loops to add moves in each direction
        :param blocked_path:
        :return:
        """
        moves = set()
        # vertically positive moves
        for i in range(1, 5):
            if not checkBounds(self.row + i):
                break
            moves.add((self.col, self.row + i))
            if (self.col, self.row + i) in blocked_path:
                break
        # vertically negetive moves
        for i in range(1, 5):
            if not checkBounds(self.row - i):
                break
            moves.add((self.col, self.row - i))
            if (self.col, self.row - i) in blocked_path:
                break
        # horizontally positive moves
        for i in range(1, 5):
            if not checkBounds(self.col + i):
                break
            moves.add((self.col + i, self.row))
            if (self.col + i, self.row) in blocked_path:
                break
        # horizontally negetive moves
        for i in range(1, 5):
            if not checkBounds(self.row - i):
                break
            moves.add((self.col, self.row - i))
            if (self.col, self.row - i) in blocked_path:
                break

        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if not (i == 0 and j == 0) and checkBounds(self.row + i) and checkBounds(self.col + i):
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

    def updateMoves(self, blocked_path=list()):
        """
        The bishop can move in four directions, to account for blockages, I shall have four loops, each loop representing one of the directions.
        """
        moves = set()
        # direction: +col, +row
        for i in range(1, 5):
            if not checkBounds(self.row + i) or not checkBounds(self.col + i):
                break
            moves.add((self.col + i, self.row + i))
            if (self.col + i, self.row + i) in blocked_path:
                break
        # direction: +col, -row
        for i in range(1, 5):
            if not checkBounds(self.row - i) or not checkBounds(self.col + i):
                break
            moves.add((self.col + i, self.row - i))
            if (self.col + i, self.row - i) in blocked_path:
                break
        # direction: -col, -row
        for i in range(1, 5):
            if not checkBounds(self.row - i) or not checkBounds(self.col - i):
                break
            moves.add((self.col - i, self.row - i))
            if (self.col - i, self.row - i) in blocked_path:
                break
        # direction: -col, +row
        for i in range(1, 5):
            if not checkBounds(self.row + i) or not checkBounds(self.col - i):
                break
            moves.add((self.col - i, self.row + i))
            if (self.col - i, self.row + i) in blocked_path:
                break

        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if not (i == 0 and j == 0) and checkBounds(self.row + i) and checkBounds(self.col + i):
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
        backwards = -1 if self.type == 'lower' else 1
        for i in directions:
            for j in directions:
                if i != 0 or j != 0 and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                    if (i, j) != (-1, backwards) and (i, j) != (1, backwards):
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
        backwards = -1 if self.type == 'lower' else 1
        if self.isPromote:
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if i != 0 or j != 0 and 0 <= self.row + i < 5 and 0 <= self.col + i < 5:
                        if (i, j) != (-1, -1) and (i, j) != (1, -1):
                            moves.add((self.col + i, self.row + j))
        else:
            banned_list = [(-1, 0), (1, 0), (0, backwards)]
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
            forward = 1 if self.type == 'lower' else -1
            if self.row + forward < 5:
                self.moves = [(self.col, self.row + forward)]

    def getMoves(self):
        return self.moves

    def promote(self):
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True
