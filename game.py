from .board import Board
from .utils import *
from .exceptions import *

class Game:
    current = 'lower'
    num_turns = 0

    def __init__(self, game_mode = 'i'):
        """
        Game mode i fro interactive and f for file

        """
        self.board = Board(game_mode)
    def executeTurn(self, inst):
        if self.num_turns >= 200:
            return 2
        self.nextTurn()

    def handle_move(self, origin, dest):
        """
        Mehtod to move piecec from origin to destination
        :param origin: origin square strign of length 2
        :param dest: origin destination square of length 2
        :return: True is sucess False is failure
        """
        if checkBounds(origin, dest):
            origin_piece = self.board.getPiece(origin)
            dest_piece = self.board.getPiece(dest)
            if origin_piece:
                if not sameTeam(origin, self.current):
                    raise WrongPlayerException("You tried to move the other player's piece.")
                if dest_piece is None:
                    """
                    Move peice
                    """
                    pass
                elif sameTeam(origin_piece, dest_piece):
                    raise MoveException("Both origin and destination is owned by you")
                if not sameTeam(origin_piece, dest_piece):
                    #capture
                    pass
            else:
                raise MoveException("No piece at origin square {}".format(origin))
        else:
            raise MoveException("Either origin or destination is out of bounds")



    def nextTurn(self):
        if self.current == "lower":
            self.current = "UPPER"
        else:
            self.current = "lower"





