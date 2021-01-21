import os
BOARD_SIZE = 5


class Board:
    """
    Class that represents the BoxShogi board
    """

    # The BoxShogi board is 5x5
    BOARD_SIZE = 5

    def __init__(self):
        self.upper_pieces = dict()
        self.lower_pieces = dict()
        self._board = self._initEmptyBoard()

    def set_lower(self, lower_dict):
        self.lower_pieces = lower_dict

    def set_upper(self, upper_dict):
        self.upper_pieces = upper_dict

    def _initEmptyBoard(self):
        lower = dict()
        upper = dict()
        board = [['' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]]
        board[0][0] = 'k'
        board[1][0] = 'g'
        board[2][0] = 's'
        board[3][0] = 'b'
        board[4][0] = 'r'
        board[0][1] = 'p'

        board[0][4] = 'K'
        board[1][4] = 'G'
        board[2][4] = 'S'
        board[3][4] = 'B'
        board[4][4] = 'R'
        board[4][3] = 'P'

        upper = {'K': 'a5', 'G': 'b5', 'S': 'c5', 'B': 'd5', 'R': 'e5', 'P': 'e4'}
        lower = {'k': 'a1', 'g': 'b1', 's': 'c1', 'b': 'd1', 'r': 'e1', 'p': 'a2'}
        self.set_lower(lower)
        self.set_upper(upper)
        return board

    def clear_pieces(self):
        self.lower_pieces = dict()
        self.upper_pieces = dict()


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
