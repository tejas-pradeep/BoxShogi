import sys
from utils import *
from game import Game
from exceptions import *


def game(game_mode='i', file_input=None):
    """
    Method runs the game. It calls executeTurn with implements the current player's turn.
    The method also checks for and handle all win conditions.
    The game runs till one of the end conditions is reached.

    Args:
        game_mode (str): The game mode, either 'i' for interactive or 'f' fro file.
        file_input (dict): Dictionary that contains piece_locations, upper_captured, lower_captured, and moves from an input file.
            (default is None)
    """
    game = Game(game_mode, file_input)
    if game_mode == 'i':
        while True:
            try:
                showBoard(game)
                printCheck(game.get_check_moves(), game.getCurrentPlayer())
                command = input(game.current + ">")
                print("{} player action: {}".format(game.current, command))
                if game.isPlayerinCheck():
                    if command not in game.get_check_moves()[1]:
                        raise MoveException("Your move does not get you out of checks")
                instruction = getMove(command)
                game.executeTurn(instruction)
            except (MoveException, WrongPlayerException, PositionOutofBoundsException, DropException) as e:

                print("\n{} player wins.  Illegal move".format(game.getPreviousPlayer()))
                print("\nWhat went wrong: {}".format(str(e)))
                quit()
            except GameEnd as e:
                # GameEnd is thrown when the game ends with a checkmate or a tie
                print(e)
            except FileParseException as e:
                print("\nWhat went wrong: {}".format(str(e)))
                quit()
    elif game_mode == 'f':
        last_command = ""
        for command in file_input['moves']:
            last_command = command
            try:
                instruction = getMove(command)
                game.executeTurn(instruction)
            except (MoveException, WrongPlayerException, PositionOutofBoundsException, DropException) as e:
                print("{} player action: {}".format(game.getCurrentPlayer(), last_command))
                showBoard(game)
                print("{} player wins. Illegal move.".format(game.getPreviousPlayer()))
                # print("\nWhat went wrong: {}".format(str(e)))
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
        printCheck(game.get_check_moves(), game.getCurrentPlayer())
        print("{}>".format(game.getCurrentPlayer()))
        quit()

def showBoard(game):
    """
    Method prints the current board state, and the pieces captured by each player.

    Args:
        game (Game): Game object that contains the current game state.
    """
    print(game.board)
    print("Captures UPPER: {}".format(" " .join(game.board.getUpperPlayer().getCaptured())))
    print("Captures lower: {}\n".format(' '.join(game.board.getLowerPlayer().getCaptured())))

def printCheck(check_tuple, current_player):
    """
    Method prints message and available moves if current player is in check.

    Args:
        check_tuple (tuple): A tuple that contains a boolean weather player is in check and a list of possible moves
        current_player (str): A string that represents the current player, either 'lower' or 'UPPER'
    """
    if check_tuple[0]:
        print("{} player is in check!".format(current_player))
        print("Available Moves: ")
        for i in check_tuple[1]:
            print(i)

def main():
    """
    Main function to read terminal input
    Calls method parseTestCase() from utils that takes in file path and returns a dictionary of the file data.
    """
    # game('f', parseTestCase("test_cases/basicCheck.in"))
    game('i')
    # if sys.argv[1] == '-f':
    #     input = parseTestCase(sys.argv[2])
    #     game('f', input)
    # if sys.argv[1] == '-i':
    #     game('i')


if __name__ == "__main__":
    main()
