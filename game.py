from board import Board
from utils import *
from exceptions import *
from piece import Piece, Preview

class Game:
    current = 'lower'
    num_turns = 0

    def __init__(self, game_mode = 'i'):
        """
        Game mode i fro interactive and f for file

        """
        self.board = Board(game_mode)

    def getCurrentPlayer(self):
        return self.current

    def executeTurn(self, inst):
        """
        Executes a move or a drop
        :param inst: instruction from command line input
        :return: 2 fro stalemate, 1 for success and 0 for failure
        """
        if self.num_turns >= 200:
            return 2
        cmd, origin, dest, promote = inst
        if cmd == 'move':
            if not promote:
                if self.checkValidPromotion(origin, dest) and isinstance(self.board.getPiece(origin), Preview):
                    raise MoveException("You did not specify the promote flag when your piece promoted.")
                self.handle_move(origin, dest)
            else:
                if not self.checkValidPromotion(origin, dest):
                    raise MoveException("You added in the promote flag when the move {} to {} does not have a promotion".format(origin, dest))
                self.handle_move(origin, dest)
                promoted_piece = self.board.getPiece(dest)
                if isinstance(promoted_piece, Piece):
                    flag = promoted_piece.promote()
                    if not flag:
                        raise MoveException("You tired to promote a piece that cannot be promoted!")


        self.nextTurn()

    def handle_move(self, origin, dest):
        """
        Method to move piecec from origin to destination
        :param origin: origin square strign of length 2
        :param dest: origin destination square of length 2
        :return: True is sucess False is failure
        """
        if checkBounds(origin, dest):
            origin_piece = self.board.getPiece(origin)
            dest_piece = self.board.getPiece(dest)
            if origin_piece and isinstance(origin_piece, Piece):
                if not sameTeam(origin_piece.getPlayerType(), self.current):
                    raise WrongPlayerException("You tried to move the other player's piece.")
                origin_piece.updateMoves()
                origin_moves = origin_piece.getMoves()
                if location_to_index(dest) not in origin_moves:
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
            else:
                raise MoveException("No piece at origin square {}".format(origin))
        else:
            raise MoveException("Either origin or destination is out of bounds")

    def checkValidPromotion(self, origin, dest):
        promotion_row = {'lower' : 4, "UPPER" : 0}
        origin_piece = self.board.getPiece(origin)
        dest_index = location_to_index(dest)
        if dest_index[1] == promotion_row[origin_piece.getPlayerType()]:
            return True
        return False




    def nextTurn(self):
        if self.current == "lower":
            self.current = "UPPER"
        else:
            self.current = "lower"
        self.num_turns += 1

    def isEnd(self):
        return False





