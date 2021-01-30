import os
from utils import *
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
        board[1][4] = Goverance('UPPER', (1, 4))
        board[2][4] = Relay('UPPER', (2, 4))
        board[3][4] = Shield("UPPER", (3, 4))
        board[4][4] = Drive("UPPER", (4, 4))
        board[4][3] = Preview("UPPER", (4, 3))

        upper = {'D': 'e5', 'G': 'b5', 'R': 'c5', 'S': 'd5', 'N': 'a5', 'P': 'e4'}
        lower = {'d': 'a1', 's': 'b1', 'r': 'c1', 'g': 'd1', 'n': 'e1', 'p': 'a2'}
        self.set_lower(lower)
        self.set_upper(upper)
        return board

    def clear_pieces(self):
        self.lower_pieces = dict()
        self.upper_pieces = dict()

    def getPiece(self, location):
        """
        Method to get the piece at location
        :param location: string of length 2 of the form like a3
        :return: piece string, example p or P
        """
        row, col = location_to_index(location)
        for p in self.pieces:
            if self._board[row][col] == p.lower():
                return p.lower()
            if self._board[row][col] == p.upper():
                return p.upper()
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
