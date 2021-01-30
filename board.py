import os
from .utils import *
from .piece import *
BOARD_SIZE = 5


class Board:
    """
    Class that represents the BoxShogi board
    """

    # The BoxShogi board is 5x5
    BOARD_SIZE = 5

    def __init__(self, game_mode):
        self.upper_pieces = dict()
        self.lower_pieces = dict()
        self.upper_captured = list()
        self.lower_captured = list()
        if game_mode == 'f':
            pass
        else:
            self._board = self._initEmptyBoard()

    def set_lower(self, lower_dict):
        self.lower_pieces = lower_dict

    def set_upper(self, upper_dict):
        self.upper_pieces = upper_dict

    def _initEmptyBoard(self):
        lower = dict()
        upper = dict()
        board = [['' for i in range(5)] for j in range(5)]
        print(board)
        board[0][0] = Drive('lower', (0, 0))
        board[1][0] = Shield('lower', (1, 0))
        board[2][0] = Relay('lower', (2, 0))
        board[3][0] = Governanace('lower', (3, 0))
        board[4][0] = Notes('lower', (4, 0))
        board[0][1] = Preview('lower', (0, 1))

        board[0][4] = Notes('UPPER', (0, 4))
        board[1][4] = Governanace('UPPER', (1, 4))
        board[2][4] = Relay('UPPER', (2, 4))
        board[3][4] = Shield("UPPER", (3, 4))
        board[4][4] = Drive("UPPER", (4, 4))
        board[4][3] = Preview("UPPER", (4, 3))

        upper = {'D': 'e5', 'G': 'b5', 'R': 'c5', 'S': 'd5', 'N': 'a5', 'P': 'e4'}
        lower = {'d': 'a1', 's': 'b1', 'r': 'c1', 'g': 'd1', 'n': 'e1', 'p': 'a2'}
        self.set_lower(lower)
        self.set_upper(upper)
        return board

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
        row, col = location_to_index(location)
        piece_at_location = self._board[row][col]
        if isinstance(piece_at_location, Piece):
            return piece_at_location
        return None



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
                s += self._stringifySquare(self._board[col][row])

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
