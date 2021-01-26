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
        return -1, -1, "Position has a length greater than 2"
    col = int(location[1])
    if col < 1 or col > 5:
        return -1, -1, "Invalid location, square {} does not exist".format(location)
    row = ord(location[0].lower()) - 97
    if row < 0 or row > 4:
        return -1, -1, "Invalid location, square {} does not exist".format(location)
    return row, col - 1


def checkBounds(origin, dest):
    o = location_to_index(origin)
    d = location_to_index(dest)
    return 5 > o[0] >= 0 and 5 > o[1] >= 0 and 5 > d[0] >= 0 and 5 > d[1] >= 0
