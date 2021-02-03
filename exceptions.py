class MoveException(Exception):
    """
    Exception raised when an illegal action is taken while trying to move a piece.
    """
    def __init__(self, message):
        super(MoveException, self).__init__(message)

class WrongPlayerException(Exception):
    """
    Exception raised when trying to access the other player's piece.
    """
    def __init__(self, message):
        super(WrongPlayerException, self).__init__(message)

class PositionOutofBoundsException(Exception):
    """
    Exception raised when an out of bounds position is inputted by the user.
    """
    def __init__(self, message):
        super(PositionOutofBoundsException, self).__init__(message)
class FileParseException(Exception):
    """
    Exception raised when an input file has corrupt data.
    """
    def __init__(self, message):
        super(FileParseException, self).__init__(message)
class GameEnd(Exception):
    """
    Exception raised when the game ends with the two proper end conditions: checkmate and tie game
    """
    def __init__(self, message):
        super(GameEnd, self).__init__(message)
class DropException(Exception):
    """
    Exception raised when an illegal action si taken when dropping a piece.
    """
    def __init__(self, message):
        super(DropException, self).__init__(message)