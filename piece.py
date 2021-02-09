import abc
# Check bounds is a method that checks if a given index is in bounds of the board
from utils import checkBounds
from board import BOARD_SIZE

class Piece(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a piece in the game.

    Attributes:
        player: player_type the piece belongs to.
        col: column index of the piece.
        row: row index of the piece.
        name: String name of the piece.
        moves : List containing all the piece's current moves.
        isPromote: boolean flag indicating if piece is promoted.

    """

    def __init__(self, player_type, index, name):
        """
        Method to initialize a piece object with passed in values.
        Method calls updateMoves to generate a starting move set for each piece.
        """
        self.player = player_type
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
        """
        Abstract method to update a piece's moves.
        """
        pass

    @abc.abstractmethod
    def getMoves(self):
        """
        Method to return a pieces move list.
        """
        pass

    def promote(self):
        """
        Method to promote a piece. By default it only adds the + sign to tis name indicating its promoted.
        """
        self.name = '+' + self.name

    def getPlayerType(self):
        """
        Method to return player who this piece belongs to.

        Returns:
            string: String representing the player.
        """
        return self.player

    def toString(self):
        """
        toString method converts a piece to its string representation.

        Returns:
            string: Representation of the piece.
        """
        if self.player.islower():
            return self.name.lower()
        else:
            return self.name.upper()

    def getIndex(self):
        """
        Method to get the piece's current index tuple.
        """
        return self.col, self.row

    def updateLocation(self, new_location):
        """
        Method to update the location of the piece.

        Args:
            new_location (tuple): index tuple representing piece's new location.
        """
        self.col = new_location[0]
        self.row = new_location[1]

    def updateSupportMoves(self, supporting_move_list):
        self.moves += supporting_move_list



class Drive(Piece):
    """
    Class representing a drive object.
    Inherits from Piece.
    """

    def __init__(self, player_type, index):
        """
        Initializing using super constructor.
        """
        super(Drive, self).__init__(player_type, index, 'd')

    def updateMoves(self, check_moves=list(), own_pieces=list()):
        """
        Method to update the moves of the drive.
        Drive can only move to locations that are not in check_moves or own_pieces.
        Args:
            check_moves (list): A list of moves that are controlled by the other player.
            own_pieces (list): A list containing locations of all the current player's pieces.
        """
        moves = set()
        directions = [-1, 0, 1]
        for i in directions:
            for j in directions:
                if i == j == 0 or not checkBounds(self.col + i) or not checkBounds(self.row + j) or (self.col + i, self.row + j) in own_pieces\
                        or (self.col + i, self.row + j) in check_moves:
                    continue
                moves.add((self.col + i, self.row + j))
        self.moves = list(moves)

    def getMoves(self):
        """
        Returns:
            list: list of index tuples containing possible moves.
        """
        return self.moves

    def promote(self):
        """
        Drive cannot be promoted, hence it returns False.
        """
        return False


class Notes(Piece):
    """
    Class representing a notes piece object.
    """
    def __init__(self, player_type, index):
        """
        Initializing object using super constructor.
        """
        super(Notes, self).__init__(player_type, index, 'n')

    def updateMoves(self, blocked_path=list()):
        """
        method to update the moves of the notes(rook) piece.
        Rook moves in four directions, to account for blockages I am using 4 loops to add moves in each direction

        Args:
            blocked_path (list): A list of current piece locations, which block the notes' path.
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
        for i in range(1, BOARD_SIZE):
            if not checkBounds(self.row - i):
                break
            moves.add((self.col, self.row - i))
            if (self.col, self.row - i) in blocked_path:
                break
        # horizontally positive moves
        for i in range(1, BOARD_SIZE):
            if not checkBounds(self.col + i):
                break
            moves.add((self.col + i, self.row))
            if (self.col + i, self.row) in blocked_path:
                break
        # horizontally negetive moves
        for i in range(1, BOARD_SIZE):
            if not checkBounds(self.col - i):
                break
            moves.add((self.col - i, self.row))
            if (self.col - i, self.row) in blocked_path:
                break

        if self.isPromote:
            # If promoted the notes can also move like a drive.
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if i == j == 0 or not checkBounds(self.col + i) or not checkBounds(self.row + j):
                        continue
                    moves.add((self.col + i, self.row + j))
        moves = list(moves)
        self.moves = moves

    def getMoves(self):
        """
        Returns:
            list: list of index tuple indicating possible moves.
        """
        return self.moves

    def promote(self):
        """
        When promoted, sets promote flag and update name and moves.
        """
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True


class Governanace(Piece):
    """
    Class representing a governance piece object.
    """
    def __init__(self, player_type, index):
        super(Governanace, self).__init__(player_type, index, 'g')

    def updateMoves(self, blocked_path=list()):
        """
        Method updates the moves of the governance(bishop).
        The bishop can move in four directions, to account for blockages, I shall have four loops, each loop representing one of the directions.

        Args:
            blocked_path (list): A list of piece locations that may block the path of the governance.
        """
        moves = set()
        # direction: +col, +row
        for i in range(1, BOARD_SIZE):
            if not checkBounds(self.row + i) or not checkBounds(self.col + i):
                break
            moves.add((self.col + i, self.row + i))
            if (self.col + i, self.row + i) in blocked_path:
                break
        # direction: +col, -row
        for i in range(1, BOARD_SIZE):
            if not checkBounds(self.row - i) or not checkBounds(self.col + i):
                break
            moves.add((self.col + i, self.row - i))
            if (self.col + i, self.row - i) in blocked_path:
                break
        # direction: -col, -row
        for i in range(1, BOARD_SIZE):
            if not checkBounds(self.row - i) or not checkBounds(self.col - i):
                break
            moves.add((self.col - i, self.row - i))
            if (self.col - i, self.row - i) in blocked_path:
                break
        # direction: -col, +row
        for i in range(1, BOARD_SIZE):
            if not checkBounds(self.row + i) or not checkBounds(self.col - i):
                break
            moves.add((self.col - i, self.row + i))
            if (self.col - i, self.row + i) in blocked_path:
                break

        if self.isPromote:
            # If promoted, governance can also move like the drive.
            directions = [-1, 0, 1]
            for i in directions:
                for j in directions:
                    if i == j == 0 or not checkBounds(self.col + i) or not checkBounds(self.row + j):
                        continue
                    moves.add((self.col + i, self.row + j))
        self.moves = list(moves)

    def getMoves(self):
        return self.moves

    def promote(self):
        """
        When promoted, sets promote flag and update name and moves.
        """
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True


class Shield(Piece):
    """
    Shield class representing a shield piece object.
    """
    def __init__(self, player_type, index):
        super(Shield, self).__init__(player_type, index, 's')

    def updateMoves(self):
        """
        Method to update the moves of the shield.
        Method makes a banned_moves list to keep track of the locations the shield cannot move to.
        """
        moves = set()
        directions = [-1, 0, 1]
        backwards = -1 if self.player == 'lower' else 1
        banned_moves = [(self.col + 1, self.row + backwards), (self.col - 1, self.row + backwards)]
        for i in directions:
            for j in directions:
                if i == j == 0 or not checkBounds(self.col + i) or not checkBounds(self.row + j) or \
                        (self.col + i, self.row + j) in banned_moves:
                    continue
                moves.add((self.col + i, self.row + j))
        moves = list(moves)
        self.moves = moves

    def getMoves(self):
        return self.moves

    def promote(self):
        """
        Shield cannot be promoted hence it return False.
        """
        return False


class Relay(Piece):
    """
    Class representing a relay piece object.
    """
    def __init__(self, player_type, index):
        super(Relay, self).__init__(player_type, index, 'r')

    def updateMoves(self):
        """
        Method to update the moves of the relay.
        Method makes a banned_moves list to keep track of the locations the relay cannot move to.
        """
        moves = set()
        directions = [-1, 0, 1]
        backwards = -1 if self.player == 'lower' else 1
        # If promoted the relay moves like the shield.
        if not self.isPromote:
            banned_moves = [(self.col + 1, self.row), (self.col - 1, self.row), (self.col, self.row + backwards)]
            for i in directions:
                for j in directions:
                    if i == j == 0 or not checkBounds(self.col + i) or not checkBounds(self.row + j) or \
                            (self.col + i, self.row + j) in banned_moves:
                        continue
                    moves.add((self.col + i, self.row + j))
        else:
            banned_moves = [(self.col + 1, self.row + backwards), (self.col - 1, self.row + backwards)]
            for i in directions:
                for j in directions:
                    if i == j == 0 or not checkBounds(self.col + i) or not checkBounds(self.row + j) or \
                            (self.col + i, self.row + j) in banned_moves:
                        continue
                    moves.add((self.col + i, self.row + j))
        self.moves = list(moves)

    def getMoves(self):
        return self.moves

    def promote(self):
        """
        When promoted, sets promote flag and update name and moves.
        """
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True


class Preview(Piece):
    """
    Class representing a preview piece object.
    """
    def __init__(self, player_type, index):
        super(Preview, self).__init__(player_type, index, 'p')

    def updateMoves(self):
        """
         Method to update the moves of the preview.
        Method makes a banned_moves list to keep track of the locations the preview cannot move to.
        """
        # If promoted, the preview moves like the box shield peice.
        if self.isPromote:
            moves = set()
            directions = [-1, 0, 1]
            backwards = -1 if self.player == 'lower' else 1
            banned_moves = [(self.col + 1, self.row + backwards), (self.col - 1, self.row + backwards)]
            for i in directions:
                for j in directions:
                    if i == j == 0 or not checkBounds(self.col + i) or not checkBounds(self.row + j) or \
                            (self.col + i, self.row + j) in banned_moves:
                        continue
                    moves.add((self.col + i, self.row + j))
            self.moves = list(moves)
        else:
            # if not promoted preview can only move one square ahead.
            forward = 1 if self.player == 'lower' else -1
            if self.row + forward < BOARD_SIZE:
                self.moves = [(self.col, self.row + forward)]

    def getMoves(self):
        return self.moves

    def promote(self):
        """
        When promoted, sets promote flag and update name and moves.
        """
        self.isPromote = True
        self.updateMoves()
        self.name = "+" + self.name
        return True
