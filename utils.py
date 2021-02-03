from exceptions import PositionOutofBoundsException, MoveException

def parseTestCase(path):
    """
    Utility function to help parse test cases.
    :param path: Path to test case file.
    """
    f = open(path)
    line = f.readline()
    initialBoardState = []
    while line != '\n':
        piece, position = line.strip().split(' ')
        initialBoardState.append(dict(piece=piece, position=position))
        line = f.readline()
    line = f.readline().strip()
    upperCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline().strip()
    lowerCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline()
    line = f.readline()
    moves = []
    while line != '':
        moves.append(line.strip())
        line = f.readline()

    return dict(initialPieces=initialBoardState, upperCaptures=upperCaptures, lowerCaptures=lowerCaptures, moves=moves)


def location_to_index(location):
    """
    Util method to convert some location on the board, a3 to its index values in the square board matrix

    Args:
        location (str): String location representing a square on the board.

    Returns:
        tuple: Index tuple containing column, row index
    """
    if len(location) != 2:
       raise PositionOutofBoundsException("Position has a length greater than 2")
    row = int(location[1])
    if row < 1 or row > 5:
        raise PositionOutofBoundsException("Invalid location, square {} does not exist".format(location))
    col = ord(location[0].lower()) - 97
    if col < 0 or col > 4:
        raise PositionOutofBoundsException("Invalid location, square {} does not exist".format(location))
    return col, row - 1

def index_to_location(index):
    """
    Util method to convert a index tuple to its square on the board.

    Args:
        index (tuple): index tuple of the form (column, row)

    Returns:
        str: string representing a square on the board.
    """
    return str(chr(ord('a') + index[0])) + str(index[1] + 1)


def checkBounds(origin, dest=None):
    """
    Util method to check is given origin and destination are in bounds.

    There are two use cases:
    1. If only origin is given: Origin is a number index.
    2. if both origin and dest are given: both origin and destination is a string representing a square.

    Args:
        origin: Either a number representing an index on the board or string representing a square on the board.
        dest (str): String representing a square on the board.
            (default value None)

    Returns:
        bool: True if in bounds else False.
    """
    if dest is None:
        return 5 > origin >= 0
    else:
        try:
            o = location_to_index(origin)
            d = location_to_index(dest)
            return 5 > o[0] >= 0 and 5 > o[1] >= 0 and 5 > d[0] >= 0 and 5 > d[1] >= 0
        except PositionOutofBoundsException:
            return False


def getMove(command):
    """
    Util method to extract a information from a command line input.

    Args:
        command: command line input.

    Returns:
        tuple: containing all the information in the command line input.
    """
    move = command.strip().split()
    (cmd, origin, dest, promote) = "move", "", "", ""
    if len(move) == 4:
        origin, dest, promote = move[1:]
    elif len(move) == 3:
        if move[0] == 'move':
            origin, dest = move[1:]
        elif move[0] == 'drop':
            cmd, origin, dest = move
        else:
            raise MoveException("Command does not have a valid move")
    promote = promote == 'promote'
    return cmd, origin, dest, promote

def sameTeam(str1, str2):
    """
    Util method to check if str1 and str2 are on the same team, ie have the same casing.
    """
    return (str1.islower() and str2.islower()) or (str1.isupper() and str2.isupper())

def isBetween(test, num1, num2):
    """
    Method to check if test number is in between num1 and num2.
    """
    return num1 < test < num2 or num2 < test < num1


