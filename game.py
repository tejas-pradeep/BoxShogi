from .board import Board
class Game:

    def __init__(self, game_mode = 'i'):
        """
        Game mode i fro interactive and f for file

        """
        self.board = Board(game_mode)