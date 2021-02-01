import os
from utils import *
from piece import *
BOARD_SIZE = 5


class Board:
    """
    Class that represents the BoxShogi board
    """

    # The BoxShogi board is 5x5
    BOARD_SIZE = 5

    def __init__(self, game_mode):
        self.upper_captured = list()
        self.lower_captured = list()
        self.lower_drive = Drive('lower', (0, 0))
        self.upper_drive = Drive('UPPER', (4, 4))
        self.upper_pieces = self.createUpperPieces()
        self.lower_pieces = self.createLowerPieces()
        self.initializeSpecialPieces()
        if game_mode == 'f':
            pass
        else:
            self._board = self._initEmptyBoard()

    def _initEmptyBoard(self):
        board = [['' for i in range(5)] for j in range(5)]
        for i in self.lower_pieces + self.upper_pieces:
            index = i.getLocation()
            board[index[0]][index[1]] = i
        return board

    def createLowerPieces(self):
        lower_pieces = [
            self.lower_drive,
            Shield('lower', (1, 0)),
            Relay('lower', (2, 0)),
            Governanace('lower', (3, 0)),
            Notes('lower', (4, 0)),
            Preview('lower', (0, 1))
        ]
        return lower_pieces

    def createUpperPieces(self):
        upper_pieces = [
            self.upper_drive,
            Notes('UPPER', (0, 4)),
            Governanace('UPPER', (1, 4)),
            Relay('UPPER', (2, 4)),
            Shield("UPPER", (3, 4)),
            Preview("UPPER", (4, 3))
        ]
        return upper_pieces

    def initializeSpecialPieces(self):
        all_pieces_location = self.getAllPieceLocations()
        for i in self.lower_pieces + self.upper_pieces:
            if isinstance(i, Notes) or isinstance(i, Governanace):
                i.updateMoves(all_pieces_location)


    def move(self, origin, dest):
        """
        Move a pice from origin to dest. Validity of moves is checked in game controller
        :param origin: origin square
        :param dest: destination square
        :return: True is sucess, False is failure
        """
        try:
            orig = location_to_index(origin)
            dest = location_to_index(dest)
            self._board[dest[0]][dest[1]] = self._board[orig[0]][orig[1]]
            self._board[orig[0]][orig[1]] = ''
            return True
        except:
            return False
    def capture(self, origin, dest):
        """
        Method to perform a capture, validity is checked by game controller
        :param origin: Origin square
        :param dest: Destination sqaure
        :return: True if sucess, false is failure
        """
        try:
            d = location_to_index(dest)
            if isinstance(self._board[d[0]][d[1]], Piece):
                captured = self.getPiece(dest)
                if captured.getPlayerType().islower():
                    self.upper_captured.append(captured.toString())
                else:
                    self.lower_captured.append(captured.toString())
            self.move(origin, dest)
            return True
        except:
            return False



    def clear_pieces(self):
        self.lower_pieces = dict()
        self.upper_pieces = dict()

    def getPiece(self, location) -> Piece:
        """
        Method to get the piece at location
        :param location: string of length 2 of the form like a3
        :return: piece string, example p or P
        """
        col, row = location_to_index(location)
        piece_at_location = self._board[col][row]
        if isinstance(piece_at_location, Piece):
            return piece_at_location
        return None

    def getAllPieceLocations(self):
        locations = list()
        for i in self.lower_pieces + self.upper_pieces:
            locations.append(i.getLocation())
        return locations

    def getAllOpponentMoves(self, current):
        opponent = {'lower': self.upper_pieces, 'UPPER': self.lower_pieces}
        moves = set()
        for i in opponent[current]:
            moves.add(i.getMoves())
        return list(moves)

    def getOpponentKing(self, current_player):
        if current_player == 'lower':
            return self.upper_drive
        else:
            return self.lower_drive


    def __repr__(self):
        return self._stringifyBoard()

    def _stringifyBoard(self):
        """
        Utility function for printing the board
        """
        s = ''
        for row in range(len(self._board) - 1, -1, -1):

            s += '' + str(row + 1) + ' |'
            for col in range(0, len(self._board[row])):
                if isinstance(self._board[col][row], Piece):
                    temp = self._board[col][row].toString()
                else:
                    temp = self._board[col][row]
                s += self._stringifySquare(temp)

            s += os.linesep

        s += '    a  b  c  d  e' + os.linesep
        return s

    def _stringifySquare(self, sq):
        """
       	Utility function for stringifying an individual square on the board

        :param sq: Array of strings.
        """
        if type(sq) is not str or len(sq) > 2:
            raise ValueError('Board must be an array of strings like "", "P", or "+P"')
        if len(sq) == 0:
            return '__|'
        if len(sq) == 1:
            return ' ' + sq + '|'
        if len(sq) == 2:
            return sq + '|'
