from board import Board
from utils import *
from exceptions import *
from piece import Piece, Preview, Notes, Governanace, Drive

class Game:
    def __init__(self, game_mode='i', file_input=None):
        """
        Game mode i for interactive and f for file

        """
        self.board = Board(game_mode, file_input)
        self.current = 'lower'
        self.opponent = 'UPPER'
        self.num_turns = 0
        self.is_check = {'lower': (False, list()), "UPPER": (False, list())}
        self.current_action = 'move'

    def getCurrentPlayer(self):
        return self.current
    def getPreviousPlayer(self):
        return self.opponent

    def get_check_moves(self):
        return self.is_check[self.getCurrentPlayer()]

    def executeTurn(self, inst):
        """
        Executes a move or a drop
        :param inst: instruction from command line input
        :throws: GameEnd when the game ends with the desired message.
        """
        if self.num_turns >= 400:
            raise GameEnd("Tie game. Too many moves")
        cmd, origin, dest, promote = inst
        self.current_action = cmd
        if cmd == 'move':
            self.is_check[self.current] = (False, list())
            if self.checkValidPromotion(origin, dest) and isinstance(self.board.getPiece(origin), Preview):
               promote = True
            if not promote:
                self.handle_move(origin, dest)
            else:
                if isinstance(self.board.getPiece(origin), Drive):
                    raise MoveException("You tired to promote the drive")
                if not self.checkValidPromotion(origin, dest):
                    raise MoveException("You added in the promote flag when the move {} to {} does not have a promotion".format(origin, dest))
                self.handle_move(origin, dest)
                promoted_piece = self.board.getPiece(dest)
                if isinstance(promoted_piece, Piece):
                    flag = promoted_piece.promote()
                    if not flag:
                        raise MoveException("You tired to promote a piece that cannot be promoted!")
        elif cmd == 'drop':
            if promote:
                raise DropException("You tried to promote a piece when dropping it.")
            self.handle_drop(origin, dest)



        self.nextTurn()

    def handle_move(self, origin, dest):
        """
        Method to move piece from origin to destination
        :param origin: origin square string of length 2
        :param dest: origin destination square of length 2
        :return: True is success False is failure
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
                    origin_piece.updateMoves(self.board.getAllOpponentMoves(self.current), self.board.getActivePieceLocations(self.current))
                else:
                    origin_piece.updateMoves()
                origin_moves = origin_piece.getMoves()
                dest_index = location_to_index(dest)
                if dest_index not in origin_moves:
                    raise MoveException("You tried to move a piece to a location it cant reach on this turn.")
                if dest_piece is None:
                    """
                    Move piece
                    """

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
                    origin_piece.updateMoves(self.board.getAllOpponentMoves(self.current), self.board.getActivePieceLocations(self.current))
                else:
                    origin_piece.updateMoves()
                self.check_for_checks(origin_piece)
            else:
                raise MoveException("No piece at origin square {}".format(origin))
        else:
            raise MoveException("Either origin or destination is out of bounds")

    def handle_drop(self, piece_type, dest):
        dest_index = location_to_index(dest)
        dest_piece = self.board.getPiece(dest)
        if dest_piece:
            raise DropException("You tried to drop a piece to a location with another piece")
        if self.current == 'lower':
           current_captured = self.board.lower_captured
           current_active = self.board.lower_pieces
           promotion_zone = 4
           piece_type = piece_type.lower()
        else:
            current_captured = self.board.upper_captured
            current_active = self.board.upper_pieces
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
        self.board.drop(piece, dest_index)
        self.check_for_checks(piece)
        current_captured.remove(piece_type)

    def check_for_checks(self, origin_piece):
        opponent_drive = self.board.getOpponentKing(self.current)
        if opponent_drive.getIndex() in origin_piece.getMoves():
            opponent_drive.updateMoves(self.board.getAllOpponentMoves(opponent_drive.getPlayerType()), self.board.getActivePieceLocations(self.opponent))
            escape_moves = self.board.getBlockMoves(origin_piece, self.opponent, opponent_drive)
            escape_moves += self.board.getCapturedEscapeMoves(origin_piece.getIndex(), self.opponent)
            escape_moves += ["move {} {}".format(index_to_location(opponent_drive.getIndex()), index_to_location(i)) for i in opponent_drive.getMoves()]
            escape_moves.sort()
            self.is_check[opponent_drive.getPlayerType()] = (True, escape_moves)
            if not escape_moves:
                self.checkmate(origin_piece)
            return True
        return False

    def checkmate(self, piece):
        """
        If opponenet king has no moves, it is a checkmate
        """
        if self.current_action == 'drop' and isinstance(piece, Preview):
            raise DropException("Cannot drop a preview piece into a checkmate.")
        raise GameEnd("{} player wins.  Checkmate.".format(self.current))


    def checkValidPromotion(self, origin, dest):
        promotion_row = {'lower': 4, "UPPER": 0}
        origin_piece = self.board.getPiece(origin)
        dest_index = location_to_index(dest)
        if dest_index[1] == promotion_row[origin_piece.getPlayerType()]:
            return True
        return False

    def nextTurn(self):
        if self.current == "lower":
            self.current = "UPPER"
            self.opponent = 'lower'
        else:
            self.current = "lower"
            self.opponent = 'UPPER'
        self.num_turns += 1

    def isPlayerinCheck(self):
        return self.is_check[self.current][0]






