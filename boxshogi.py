import sys
from .utils import *
from .game import Game

def game(game_mode = 'i'):
    game = Game(game_mode)
    game_end = False
    while not game_end:
        command = input()
        instruction = getMove(command)
def main():
    """
    Main function to read terminal input
    """
    if sys.argv[1] == '-f':
        input = parseTestCase(sys.argv[2])
        # Prints example output
        print(
"""UPPER player action: drop s d1
5 |__|__| R|__| D|
4 |__|__|__|__|__|
3 |__|__|__|__|__|
2 |__|__|__|__|__|
1 | d| g|__| n|__|
    a  b  c  d  e

Captures UPPER: S R P
Captures lower: p n g s

lower player wins.  Illegal move.""")
        game('f')

    if sys.argv[1] == '-i':
        game('i')

if __name__ == "__main__":
    main()