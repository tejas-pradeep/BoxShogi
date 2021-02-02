import sys
from utils import *
from game import Game
from exceptions import *


def game(game_mode='i', file_input=None):
    game = Game(game_mode, file_input)
    if game_mode == 'i':
        while True:
            try:
                showBoard(game)
                isCheck(game.get_check_moves(), game.getCurrentPlayer())
                command = input(game.current + ">")
                print("{} player action: {}".format(game.current, command))
                if game.isPlayerinCheck():
                    if command not in game.get_check_moves()[1]:
                        raise MoveException("Your move does not get you out of checks")
                instruction = getMove(command)
                game.executeTurn(instruction)
            except (MoveException, WrongPlayerException, PositionOutofBoundsException, DropException) as e:
                print("\n{} player wins. Illegal move".format(game.getPreviousPlayer()))
                print("\nWhat went wrong: {}".format(str(e)))
                quit()
            except GameEnd as e:
                print(e)
            except FileParseException as e:
                print(e)
                quit()
    elif game_mode == 'f':
        last_command = ""
        for command in file_input['moves']:
            last_command = command
            try:
                instruction = getMove(command)
                game.executeTurn(instruction)
            except (MoveException, WrongPlayerException, PositionOutofBoundsException, DropException) as e:
                showBoard(game)
                print("{} player wins. Illegal move.".format(game.getPreviousPlayer()))
                quit()
            except GameEnd as e:
                print("{} player action: {}".format(game.getCurrentPlayer(), command))
                showBoard(game)
                print("{}".format(str(e)))
                quit()
            except FileParseException as e:
                print("{}".format(str(e)))
                quit()
        print("{} player action: {}".format(game.getPreviousPlayer(), last_command))
        showBoard(game)
        isCheck(game.get_check_moves(), game.getCurrentPlayer())
        print("{}>".format(game.getCurrentPlayer()))
        quit()

def showBoard(game):
    print(game.board)
    print("Captures UPPER: {}".format(" " .join(game.board.upper_captured)))
    print("Captures lower: {}\n".format(' '.join(game.board.lower_captured)))

def isCheck(check_tuple, current_player):
    """
    Method check tuple prints message and available moves if current player is in check.
    :param check_tuple: IS a tuple containing a boolean at index 0, which indicates weather the current player is in check.
    And a list at index 1 containing possible moves.
    """
    if check_tuple[0]:
        print("{} player is in check!".format(current_player))
        print("Available Moves: ")
        for i in check_tuple[1]:
            print(i)



def main():
    """
    Main function to read terminal input
    """
    # game('f', parseTestCase('test_cases/blockOutOfCheck.in'))
    # game('i')
    if sys.argv[1] == '-f':
        input = parseTestCase(sys.argv[2])
        game('f', input)
    if sys.argv[1] == '-i':
        game('i')


if __name__ == "__main__":
    main()
