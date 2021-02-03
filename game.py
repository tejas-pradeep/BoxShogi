from board import Board
from utils import *
from exceptions import *
from piece import Piece, Preview, Notes, Governanace, Drive, Shield

class Game:
    """
    Game class represents the game state. All the game's moving parts occur through this class.

    Attributes:
        board (Board): The current game board.
        current (str): The current active player.
        opponent (str): The current player's opponent.
        num_turns (int): The number of turns that have occurred. A turn is an action done by both players.
        is_check (Mapping[str -> (boolean, list)]): A mapping from player_type(str) to a
            tuple that contains weather the player is in check, and a list of available moves.
        current_action (str): A string representing the current action being executed, either 'move' or 'drop'
    """
    def __init__(self, game_mode='i', file_input=None):
        """
        Initialize all the attributes with its start state values.

        Args:
            self (Game): Current game object accessing the method
            game_mode (str): Indicates either interactive mode or File mode.
                (default value 'i')
            file_input (dict): Dictionary that contains piece_locations, upper_captured, lower_captured, and moves from an input file.
            (default is None)
        """
        self.board = Board(game_mode, file_input)
        self.current = 'lower'
        self.opponent = 'UPPER'
        self.num_turns = 0
        self.is_check = {'lower': (False, list()), "UPPER": (False, list())}
        self.current_action = 'move'

    def getCurrentPlayer(self) -> str:
        """
        Method returns the current active player.

        Returns:
            str: Current active player.
        """
        return self.current
    def getPreviousPlayer(self):
        """
        Method returns the opponent of the current player, ie the other player.

        Returns:
            str: The other player.
        """
        return self.opponent

    def get_check_moves(self):
        """
        Method returns the is_check value for the current player.

        Return:
            (bool, list): A boolean representing if current player is in check, A list containing the available moves
        """
        return self.is_check[self.getCurrentPlayer()]

    def executeTurn(self, inst):
        """
        Method executes a player turn.
        It checks for promotion and drop illegal moves.
        Calls methods handleMove() and handleDrop() to implement a move or a drop.

        Args:
            inst (tuple): A tuple that contains command (move or drop), origin location, destination location, promote: A boolean is promote flag is given.

        Raises:
            MoveException: When any illegal action is taken for a move command.
            DropException: When any illegal action is taken for a drop command.
            WrongPlayerException: When player tries to move the piece of the opposite player.
            GameEnd: When the game ends in either a tie or a checkmate.
        """
        cmd, origin, dest, promote = inst
        self.current_action = cmd
        if cmd == 'move':
            self.refreshCheck()
            # Even if promote flag is not specified, Preview promotes by default on the last row.
            if self.checkValidPromotion(origin, dest) and isinstance(self.board.getPiece(origin), Preview):
               promote = True
            # Checking for promotion illegal moves
            if promote:
                piece = self.board.getPiece(origin)
                if piece.isPromote:
                    raise MoveException("You tried to promote a piece that is already promoted.")
                if isinstance(piece, Drive) or isinstance(piece, Shield):
                    raise MoveException("You tired to promote a piece that cannot be promoted.")
                if not self.checkValidPromotion(origin, dest):
                    raise MoveException("You added in the promote flag when the move {} to {} does not have a promotion".format(origin, dest))
                self.handleMove(origin, dest)
                piece.promote()
            else:
                self.handleMove(origin, dest)
        elif cmd == 'drop':
            if promote:
                raise DropException("You tried to promote a piece when dropping it.")
            self.handleDrop(origin, dest)
        self.nextTurn()

    def handleMove(self, origin, dest):
        """
        Method to move piece from origin to destination.
        Method checks for illegal actions on trying to move a piece.
        Method calls util function location_to_index() that converts a square location. like a1 to its index (0, 0)
        method calls util function sameteam() which checks if the two arguments are on the same team.

        Args:
            origin (str): Piece origin square string. The location is a square on the board like a3.
            dest (str): piece destination square. the location is a square on the board like a3.

        Raises:
            WrongPlayerException: When player tires to move the other player's piece.
            MoveException: When players takes an illegal action when trying to move the piece.


        """
        if checkBounds(origin, dest):
            origin_piece = self.board.getPiece(origin)
            dest_piece = self.board.getPiece(dest)
            if origin_piece and isinstance(origin_piece, Piece):
                if not sameTeam(origin_piece.getPlayerType(), self.current):
                    raise WrongPlayerException("You tried to move the other player's piece.")
                if isinstance(origin_piece, Notes) or isinstance(origin_piece, Governanace):
                    origin_piece.updateMoves(self.board.getAllPieceLocations())
                elif isinstance(origin_piece, Drive):
                    origin_piece.updateMoves(self.board.getAllMoves(self.opponent), self.board.getActivePieceLocations(self.current))
                else:
                    origin_piece.updateMoves()
                origin_moves = origin_piece.getMoves()
                dest_index = location_to_index(dest)
                if dest_index not in origin_moves:
                    raise MoveException("You tried to move a piece to a location it cant reach on this turn.")
                if self.isPinned(origin_piece, dest_index):
                    raise MoveException("You tried to move a pinned piece.")
                if dest_piece is None:
                    self.board.move(origin, dest)
                elif sameTeam(origin_piece.getPlayerType(), dest_piece.getPlayerType()):
                    raise MoveException("Both origin and destination is owned by you")
                else:
                    self.board.capture(origin, dest)
                    self.board.removePiece(dest_piece, self.opponent)
                origin_piece.updateLocation(dest_index)
                if isinstance(origin_piece, Notes) or isinstance(origin_piece, Governanace):
                    origin_piece.updateMoves(self.board.getAllPieceLocations())
                elif isinstance(origin_piece, Drive):
                    origin_piece.updateMoves(self.board.getAllMoves(self.opponent), self.board.getActivePieceLocations(self.current))
                else:
                    origin_piece.updateMoves()
                ret_value = self.check_for_checks(origin_piece)
                if ret_value == 'checkmate':
                    raise GameEnd("{} player wins.  Checkmate.".format(self.current))
            else:
                raise MoveException("No piece at origin square {}".format(origin))
        else:
            raise MoveException("Either origin or destination is out of bounds")

    def handleDrop(self, piece_type, dest):
        dest_index = location_to_index(dest)
        dest_piece = self.board.getPiece(dest)
        if dest_piece:
            raise DropException("You tried to drop a piece to a location with another piece")
        if self.current == 'lower':
           current_captured = self.board.getLowerPlayer().getCaptured()
           current_active = self.board.getLowerPlayer().getPieces()
           promotion_zone = 4
           piece_type = piece_type.lower()
        else:
            current_captured = self.board.getUpperPlayer().getCaptured()
            current_active = self.board.getUpperPlayer().getPieces()
            promotion_zone = 0
            piece_type = piece_type.upper()
        piece_type = piece_type if piece_type in current_captured else '+' + piece_type
        if piece_type not in current_captured:
            raise DropException("You tried to drop a piece you have not captured.")
        if piece_type.lower() == 'p':
            for i in current_active:
                if isinstance(i, Preview) and dest_index[0] == i.getIndex()[0]:
                    raise DropException("Tried to drop a preview piece into a column with another preview.")
            if dest_index[1] == promotion_zone:
                raise DropException("You tried to drop a preview ont a spot that results in promotion.")
        piece = Board.createPieceFromName(piece_type[-1], self.current, dest_index)
        current_active.append(piece)
        ret_value = self.check_for_checks(piece)
        self.board.drop(piece, dest_index)
        current_captured.remove(piece_type)
        if ret_value == 'checkmate':
            raise GameEnd("{} player wins.  Checkmate.".format(self.current))

    def check_for_checks(self, origin_piece):
        opponent_drive = self.board.getPlayerDrive(self.opponent)
        possible_checks = origin_piece.getMoves()
        # Checking for discovered attacks.
        possible_checks.extend(self.board.getNotesGovernanceMoves(self.current))
        if opponent_drive.getIndex() in possible_checks:
            opponent_drive.updateMoves(self.board.getAllMoves(self.current), self.board.getActivePieceLocations(self.opponent))
            escape_moves = self.board.getBlockMoves(origin_piece, opponent_drive)
            escape_moves += self.board.getCapturedEscapeMoves(origin_piece.getIndex(), self.opponent)
            escape_moves += ["move {} {}".format(index_to_location(opponent_drive.getIndex()), index_to_location(i)) for i in opponent_drive.getMoves()]
            escape_moves.sort()
            self.is_check[opponent_drive.getPlayerType()] = (True, escape_moves)
            if not escape_moves:
                return self.checkmate(origin_piece)
            return True
        return False
    def checkmate(self, piece):
        """
        If opponenet king has no moves, it is a checkmate
        """
        if self.current_action == 'drop' and isinstance(piece, Preview):
            raise DropException("Cannot drop a preview piece into a checkmate.")
        return 'checkmate'

    def checkValidPromotion(self, origin, dest):
        promotion_row = {'lower': 4, "UPPER": 0}
        origin_piece = self.board.getPiece(origin)
        dest_index = location_to_index(dest)
        origin_index = location_to_index(origin)
        if dest_index[1] == promotion_row[origin_piece.getPlayerType()] or origin_index[1] == promotion_row[origin_piece.getPlayerType()]:
            return True

        return False

    def isPinned(self, piece, dest_index):
        current_king = self.board.getPlayerDrive(self.current)
        origin_index = piece.getIndex()
        piece.updateLocation(dest_index)
        possible_checks = self.board.getNotesGovernanceMoves(self.opponent)
        piece.updateLocation(origin_index)
        if current_king.getIndex() in possible_checks:
            return True
        return False

    def nextTurn(self):
        if self.current == "lower":
            self.current = "UPPER"
            self.opponent = 'lower'
        else:
            self.num_turns += 1
            if self.num_turns >= 200:
                raise GameEnd("Tie game.  Too many moves.")
            self.current = "lower"
            self.opponent = 'UPPER'

    def isPlayerinCheck(self):
        return self.is_check[self.current][0]

    def refreshCheck(self):
        self.is_check[self.current] = (False, list())






