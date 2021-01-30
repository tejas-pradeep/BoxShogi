from .exceptions import PositionOutofBoundsException, MoveException

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
    :param location: string of length 2, example a3
    :return: a tuple containing (row, column) indices.
    """
    if len(location) != 2:
       raise PositionOutofBoundsException("Position has a length greater than 2")
    col = int(location[1])
    if col < 1 or col > 5:
        raise PositionOutofBoundsException("Invalid location, square {} does not exist".format(location))
    row = ord(location[0].lower()) - 97
    if row < 0 or row > 4:
        raise PositionOutofBoundsException("Invalid location, square {} does not exist".format(location))
    return row, col - 1


def checkBounds(origin, dest):
    try:
        o = location_to_index(origin)
        d = location_to_index(dest)
        return 5 > o[0] >= 0 and 5 > o[1] >= 0 and 5 > d[0] >= 0 and 5 > d[1] >= 0
    except PositionOutofBoundsException:
        return False


def getMove(command):
    move = command.strip().split()
    returnTuple = (cmd, origin, dest, promote) = "move", "", "", ""
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
    return returnTuple

def sameTeam(str1, str2):
    return (str1.isLower() and str2.isLower()) or (str1.isUpper() and str2.isUpper())


