import os
from utils import *
from piece import *
from exceptions import FileParseException
from player import Player

BOARD_SIZE = 5

class Board:
    """
    Board class represents the current board state. All actions on the board happen through this class.
    Methods in this class also give information about current piece locations and moves on the board.

    Attributes:
        lower_player (Player): player object representing the lower player.
        upper_player (Player): player object representing the upper player.
        players (dist): A mapping from player name to its object.
        _board (matrix): A 5x5 matrix of empty strings and Piece objects representing the current board.
    """
    def __init__(self, game_mode, file_input=None):
        """
        Initialize all the attributes with its start state values.

        Args:
            game_mode (str): either 'i' or 'f' to represent interactive and file mode.
            file_input (dict): A dictionary that contains all the data from a file input.
                (default value None when interactive mode)
        """
        self.lower_player = Player('lower')
        self.upper_player = Player('UPPER')
        self.players = {'lower': self.lower_player, 'UPPER': self.upper_player}
        if game_mode == 'f':
            self._initFilePieces(file_input)
            self._board = self._initBoard()
        else:
            self.createUpperPieces()
            self.createLowerPieces()
            self._board = self._initBoard()
        self.initializeSpecialPieces()

    def _initBoard(self):
        """
        Method to initialize the board with current player pieces at their locations.

        Returns:
            Matrix: A 5x5 matrix representing the game board.
        """
        board = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        for i in self.lower_player.getPieces() + self.upper_player.getPieces():
            index = i.getIndex()
            board[index[0]][index[1]] = i
        return board

    def _initFilePieces(self, file_input):
        """
        Method to initialize pieces from file_input.
        The file_input gives each active a piece a location on the board.

        Args:
            file_input (dist): Dictionary representing data from the file.

        Raises:
            FileParseException: Exception thrown if there is some issue with the file leading to corrupted file_input data.
        """
        piece_dict = {
            'd': self.lower_player.getDrive(),
            'n': Notes('lower', (0, 0)),
            's': Shield('lower', (0, 0)),
            'r': Relay('lower', (0, 0)),
            'g': Governanace('lower', (0, 0)),
            'p': Preview('lower', (0, 0)),
            'D': self.upper_player.getDrive(),
            'N': Notes('UPPER', (0, 0)),
            'S': Shield('UPPER', (0, 0)),
            'R': Relay('UPPER', (0, 0)),
            'G': Governanace('UPPER', (0, 0)),
            'P': Preview('UPPER', (0, 0)),
        }
        try:
            for i in file_input['initialPieces']:
                # Accounting for promoted pieces.
                if len(i['piece']) == 2:
                    piece_dict[i['piece'][1]].promote()
                    i['piece'] = i['piece'][1]
                piece = piece_dict[i['piece']]
                piece.updateLocation(location_to_index(i['position']))
                if piece.getPlayerType() == 'lower':
                    self.lower_player.addPiece(piece)
                else:
                    self.upper_player.addPiece(piece)
            self.upper_player.setCaptured(file_input['upperCaptures'])
            self.lower_player.setCaptured(file_input['lowerCaptures'])
        except:
            raise FileParseException("Error while parsing input file.")

    def initializeSpecialPieces(self):
        """
        Method to initialize notes and governance's moves since their move set depends on location of all other pieces.
        """
        all_pieces_location = self.getAllPieceLocations()
        for i in self.lower_player.getPieces() + self.upper_player.getPieces():
            if isinstance(i, Notes) or isinstance(i, Governanace):
                i.updateMoves(all_pieces_location)

    def getLowerPlayer(self):
        """
        Returns lower player object.

        Returns:
            Player: lower player object.
        """
        return self.lower_player

    def getUpperPlayer(self):
        """
        Returns upper player object.

        Returns:
            Player: upper player object.
        """
        return self.upper_player

    def createLowerPieces(self):
        """
        Creates lower player's pieces when game is in interactive mode.
        Method assigns to the lower_player.
        """
        lower_pieces = [
            self.lower_player.getDrive(),
            Shield('lower', (1, 0)),
            Relay('lower', (2, 0)),
            Governanace('lower', (3, 0)),
            Notes('lower', (4, 0)),
            Preview('lower', (0, 1))
        ]
        self.lower_player.setPieces(lower_pieces)

    def createUpperPieces(self):
        """
        Creates upper player's pieces when game is in interactive mode.
        Method assigns to the upper_player.
        """
        upper_pieces = [
            self.upper_player.getDrive(),
            Notes('UPPER', (0, 4)),
            Governanace('UPPER', (1, 4)),
            Relay('UPPER', (2, 4)),
            Shield("UPPER", (3, 4)),
            Preview("UPPER", (4, 3))
        ]
        # Both drives initially created with (0, 0) location.
        self.upper_player.getDrive().updateLocation((4, 4))
        self.upper_player.setPieces(upper_pieces)

    def move(self, origin, dest):
        """
        Move a piece from origin to dest. Validity of moves is checked in game controller
        Method calls util function location_to_index to convert a string square to its index tuple.
        Args:
            origin (str): Origin square of the form like a1
            dest (str): Destination square of the form like a1
        """
        orig = location_to_index(origin)
        dest = location_to_index(dest)
        self._board[dest[0]][dest[1]] = self._board[orig[0]][orig[1]]
        self._board[orig[0]][orig[1]] = ''

    def capture(self, origin, dest):
        """
        Method to perform a capture, validity is checked by game controller
        Method calls util function location_to_index to convert a string square to its index tuple.

        Args:
            origin (str): Origin square of the form like a1
            dest (str): Destination square of the form like a1
        """
        d = location_to_index(dest)
        if isinstance(self._board[d[0]][d[1]], Piece):
            captured = self.getPiece(dest)
            if captured.getPlayerType().islower():
                self.upper_player.addCapture(captured.toString()[-1].upper())
            else:
                self.lower_player.addCapture(captured.toString()[-1].lower())
        self.move(origin, dest)

    def drop(self, piece, index):
        """
        Method to drop a piece to an index. Illegal action checks done by game controller.

        Args:
            piece (Piece): Piece to be dropped.
            index (tuple): Index tuple representing destination.
        """
        self._board[index[0]][index[1]] = piece

    def removePiece(self, piece, player):
        """
        Method to remove a piece from a player.

        Args:
            piece (Piece): Piece object to be removed.
            player (str): String representing player to be removed from.
        """
        if player == 'lower':
            self.lower_player.removePiece(piece)
        else:
            self.upper_player.removePiece(piece)

    def getPiece(self, location) -> Piece:
        """
        Method to get the piece at location
        Method calls util function location_to_index to convert a string square to its index tuple.
        Args:
            location (str): String location square of the form like a1.

        Return:
            None: If no piece is at the location.
            Piece: If a piece exists at the location.
        """
        col, row = location_to_index(location)
        piece_at_location = self._board[col][row]
        if isinstance(piece_at_location, Piece):
            return piece_at_location
        return None

    def getAllPieceLocations(self, remove_drive=None):
        """
        Method returns a list of all piece locations.
        Method is used to detect blockages for notes and governance pieces.

        Args:
            remove_drive (Drive): The opposition drive cannot block the piece as it results in a check.
                (default value None)

        Returns:
            list: List of all piece locations, except remove_drive
        """
        locations = list()
        for i in self.lower_player.getPieces() + self.upper_player.getPieces():
            if i == remove_drive:
                continue
            locations.append(i.getIndex())
        return locations

    def getActivePieceLocations(self, player):
        """
        Method returns a list containing a location of all of player's pieces.

        Args:
            player (str): String representing the player.

        Returns:
            list: List with locations of all of player's pieces.
        """
        blocked_location = set()
        for i in self.players[player].getPieces():
            blocked_location.add(i.getIndex())
        return list(blocked_location)

    def getAllMoves(self, player):
        """
        Method gets a list of possible squares player's pieces currently control.
        This list is used for detecting illegal moves for drive, since it cannot move into check.

        Args:
            player (str): String representing the player.

        Returns:
            list: List containing every square player (index tuple) currently controls.
        """
        moves = set()
        opponent_player = 'UPPER' if player == 'lower' else 'lower'
        for i in self.players[player].getPieces():
            if isinstance(i, Notes) or isinstance(i, Governanace):
                i.updateMoves(self.getAllPieceLocations(self.players[opponent_player].getDrive()))
            else:
                i.updateMoves()
            moves.update(i.getMoves())
        return list(moves)

    def getPlayerDrive(self, player):
        """
        Method to get player's drive (king)

        Args:
             player (str): String representing the player.

        Returns:
            Drive: player's drive object.
        """
        return self.players[player].getDrive()

    def getCapturedEscapeMoves(self, piece_location, player):
        """
        Method gets all possible moves player can take to capture piece at passed in location.
        Method is used to get escape moves when in check.

        Args:
            piece_location (tuple): tuple index indicating a piece's current location.
            player (str): Player trying to capture piece at location piece_location.

        Returns:
            list: Of moves (index tuples) that can result in a capture.
        """
        capture_moves = set()
        for i in self.players[player].getPieces():
            if isinstance(i, Drive):
                continue
            i.updateMoves()
            for j in i.getMoves():
                if j == piece_location:
                    capture_moves.add("move {} {}".format(index_to_location(i.getIndex()), index_to_location(j)))
        return capture_moves

    def getBlockMoves(self, attack_piece, defend_king):
        """
        Method to get a list of moves to block a check by moving a piece in the way or dropping a piece in the way.

        This method has two section.
        1. Block the check with a drop move.
        2. Block the check by moving an active piece.

        isBetween is a util method that return true if some test value is in between the two other arguments.

        Args:
            attack_piece (Piece): Piece currently attacking the opponent's drive.
            defend_king (Drive): Drive object currently under check.

        Returns:
            list: of full move strings of the form ("move a2 a3"), which can result in a block of the check.
        """
        # Setup: Getting the path between the king and attacking piece #
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

        # 1. Drop Moves #

        for index in path_between_pieces:
            for piece_name in self.players[defend_king.getPlayerType()].getCaptured():
                block_moves.append("drop {} {}".format(piece_name.lower(), index_to_location(index)))

        # 2. Block by moving a piece #

        for piece in self.players[defend_king.getPlayerType()].getPieces():
            if isinstance(piece, Drive):
                continue
            for move in piece.getMoves():
                if move in path_between_pieces:
                    block_moves.append("move {} {}".format(index_to_location(piece.getIndex()), index_to_location(move)))

        return block_moves

    def getNotesGovernanceMoves(self, player, piece=None):
        """
        Method to return the current moves of player's notes and governance pieces.
        Used to detect pins and discovered attacks.
        Args:
            player (str): Player string representing the player under examine.
            piece (Piece): A piece object representing a piece that on tis current move captures the notes or governance.
                (default value None)

        Returns:
            list: containing all squares (index tuples) controlled by player's notes and governance
        """
        moves = []
        for i in self.players[player].getPieces():
            if isinstance(i, Notes) or isinstance(i, Governanace):
                # To account for captures.
                if piece and i.getIndex() == piece.getIndex():
                    continue
                i.updateMoves(self.getAllPieceLocations())
                moves.extend(i.getMoves())
        return moves

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
        """
        Static method used to create a piece from its string representation.
        Used to create file input pieces.

        Args:
            name (str): Piece name
            player_type (str): Player who this piece belongs to.
            index (tuple): piece's location

        Returns:
            Piece: Newly created piece.
        """
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
