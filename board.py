import os
from utils import *
from piece import *
from exceptions import FileParseException
BOARD_SIZE = 5


class Board:
    """
    Class that represents the BoxShogi board
    """

    # The BoxShogi board is 5x5
    BOARD_SIZE = 5

    def __init__(self, game_mode, file_input=None):
        self.upper_captured = list()
        self.lower_captured = list()
        self.lower_drive = Drive('lower', (0, 0))
        self.upper_drive = Drive('UPPER', (4, 4))
        self.upper_pieces = list()
        self.lower_pieces = list()
        if game_mode == 'f':
            self._initFilePieces(file_input)
            self._board = self._initBoard()
        else:
            self.upper_pieces = self.createUpperPieces()
            self.lower_pieces = self.createLowerPieces()
            self._board = self._initBoard()
        self.initializeSpecialPieces()

    def _initBoard(self):
        board = [['' for i in range(5)] for j in range(5)]
        for i in self.lower_pieces + self.upper_pieces:
            index = i.getIndex()
            board[index[0]][index[1]] = i
        return board

    def _initFilePieces(self, file_input):
        piece_dict = {
            'd': self.lower_drive,
            'n': Notes('lower', (0, 0)),
            's': Shield('lower', (0, 0)),
            'r': Relay('lower', (0, 0)),
            'g': Governanace('lower', (0, 0)),
            'p': Preview('lower', (0, 0)),
            'D': self.upper_drive,
            'N': Notes('UPPER', (0, 0)),
            'S': Shield('UPPER', (0, 0)),
            'R': Relay('UPPER', (0, 0)),
            'G': Governanace('UPPER', (0, 0)),
            'P': Preview('UPPER', (0, 0)),
        }
        try:
            for i in file_input['initialPieces']:
                if len(i['piece']) == 2:
                    piece_dict[i['piece'][1]].promote()
                    i['piece'] = i['piece'][1]
                piece = piece_dict[i['piece']]
                piece.updateLocation(location_to_index(i['position']))
                if piece.getPlayerType() == 'lower':
                    self.lower_pieces.append(piece)
                else:
                    self.upper_pieces.append(piece)
            self.upper_captured = file_input['upperCaptures']
            self.lower_captured = file_input['lowerCaptures']
        except:
            raise FileParseException("Error while parsing input file.")

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
                    self.upper_captured.append(captured.toString()[-1].upper())
                else:
                    self.lower_captured.append(captured.toString()[-1].lower())
            self.move(origin, dest)
            return True
        except:
            return False
    def drop(self, piece, index):
        self._board[index[0]][index[1]] = piece

    def removePiece(self, piece, player):
        if player == 'lower':
            self.lower_pieces.remove(piece)
        else:
            self.upper_pieces.remove(piece)

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

    def getAllPieceLocations(self, remove_drive=None):
        locations = list()
        for i in self.lower_pieces + self.upper_pieces:
            if i == remove_drive:
                continue
            locations.append(i.getIndex())
        return locations

    def getActivePieceLocations(self, player):
        current_player = {'lower': self.lower_pieces, 'UPPER': self.upper_pieces}
        blocked_location = set()
        for i in current_player[player]:
            blocked_location.add(i.getIndex())
        return list(blocked_location)


    def getAllOpponentMoves(self, active_player):
        opponent = {'lower': self.upper_pieces, 'UPPER': self.lower_pieces}
        active_drive = {'lower': self.lower_drive, 'UPPER': self.upper_drive}
        moves = set()
        for i in opponent[active_player]:
            if isinstance(i, Notes) or isinstance(i, Governanace):
                i.updateMoves(self.getAllPieceLocations(active_drive[active_player]))
            else:
                i.updateMoves()
            moves.update(i.getMoves())
        return list(moves)

    def getOpponentKing(self, player):
        if player == 'lower':
            return self.upper_drive
        else:
            return self.lower_drive

    def getCapturedEscapeMoves(self, piece_location, player):
        active_pieces = {'lower': self.lower_pieces, 'UPPER': self.upper_pieces}
        capture_moves = set()
        for i in active_pieces[player]:
            if isinstance(i, Drive):
                continue
            i.updateMoves()
            for j in i.getMoves():
                if j == piece_location:
                    capture_moves.add("move {} {}".format(index_to_location(i.getIndex()), index_to_location(j)))
        return capture_moves
    def getBlockMoves(self, attack_piece, attack_player, defend_king):
        """
        This method has two section.
        1. Block the check with a drop move.
        2. Block the check by moving an active piece.
        isBetween is a util method that return tru if some test value is in between the two other arguments.
        """
        ### Setup: Getting the squares between the king and attacking piece
        block_moves = list()
        path_between_pieces = list()
        drive_location = defend_king.getIndex()
        attack_location = attack_piece.getIndex()
        if isinstance(attack_piece, Notes):
            for i in attack_piece.getMoves():
                if i[0] == drive_location[0] and isBetween(i[1], attack_location[1], drive_location[1]):
                    path_between_pieces.append(i)
                if i[1] == drive_location[1] and isBetween(i[0], attack_location[0], drive_location[0]):
                    path_between_pieces.append(i)
        elif isinstance(attack_piece, Governanace):
            for i in attack_piece.getMoves():
                if isBetween(i[0], attack_location[0], drive_location[0]) and isBetween(i[1], attack_location[1], drive_location[1]):
                    path_between_pieces.append(i)
        else:
            return []

        ### 1. Drop Moves ###

        captured_list = {'lower': self.lower_captured, 'UPPER': self.upper_captured}
        for index in path_between_pieces:
            for piece_name in captured_list[defend_king.getPlayerType()]:
                block_moves.append("drop {} {}".format(piece_name.lower(), index_to_location(index)))

        ### 2. Block by moving a piece ###

        piece_list = {'lower': self.lower_pieces, 'UPPER': self.upper_pieces}
        for piece in piece_list[defend_king.getPlayerType()]:
            if isinstance(piece, Drive):
                continue
            for move in piece.getMoves():
                if move in path_between_pieces:
                    block_moves.append("move {} {}".format(index_to_location(piece.getIndex()), index_to_location(move)))

        return block_moves






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

    @staticmethod
    def createPieceFromName(name, player_type, index):
        piece_type = name.lower()
        if piece_type == 'p':
            return Preview(player_type, index)
        if piece_type == 'g':
            return Governanace(player_type, index)
        if piece_type == 's':
            return Shield(player_type, index)
        if piece_type == 'r':
            return Relay(player_type, index)
        if piece_type == 'n':
            return Notes(player_type, index)
        return None
