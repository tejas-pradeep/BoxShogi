import sys
from utils import *
from game import Game
from board import Board
from exceptions import *


def game(game_mode='i'):
    game = Game(game_mode)
    game_end = False
    while not game_end:
        try:
            showBoard(game)
            isCheck(game.get_check_moves(), game.getCurrentPlayer())
            command = input(game.current + ">")
            print("{} player action: {}".format(game.current, command))
            instruction = getMove(command)
            game.executeTurn(instruction)
            game_end = game.isEnd()
        except (MoveException, WrongPlayerException, PositionOutofBoundsException) as e:
            print("\n------------------------------\n")
            print("{} player wins. Illegal move".format(game.getCurrentPlayer()))
            print("\nWhat went wrong: {}".format(str(e)))
            quit()  


def showBoard(game):
    print(game.board)
    print("Captures UPPER: {}".format(" " .join(game.board.upper_captured)))
    print("Captures lower: {}".format(' '.join(game.board.lower_captured)))
    print('')

def isCheck(check_tuple, current_player):
    """
    Method check tuple prints message and available moves if current player is in check.
    :param check_tuple: IS a tuple containing a boolean at index 0, which indicates weather the current player is in check.
    And a list at index 1 containing possible moves.
    """
    if check_tuple[0]:
        print("\n {} player is in check!".format(current_player))
        print("Available moves: {}".format(' '.join(check_tuple[1])))



def main():
    """
    Main function to read terminal input
    """
    game('-i')
#     if sys.argv[1] == '-f':
#         input = parseTestCase(sys.argv[2])
#         # Prints example output
#         print(
#             """UPPER player action: drop s d1
# 5 |__|__| R|__| D|
# 4 |__|__|__|__|__|
# 3 |__|__|__|__|__|
# 2 |__|__|__|__|__|
# 1 | d| g|__| n|__|
#     a  b  c  d  e
#
# Captures UPPER: S R P
# Captures lower: p n g s
#
# lower player wins.  Illegal move.""")
#         game('f')
#
#     if sys.argv[1] == '-i':
#         game('i')


if __name__ == "__main__":
    main()
