class MoveException(Exception):
    def __init__(self, message):
        super(MoveException, self).__init__(message)

class WrongPlayerException(Exception):
    def __init__(self, message):
        super(WrongPlayerException, self).__init__(message)

class PositionOutofBoundsException(Exception):
    def __init__(self, message):
        super(PositionOutofBoundsException, self).__init__(message)
class FileParseException(Exception):
    def __init__(self, message):
        super(FileParseException, self).__init__(message)
class GameEnd(Exception):
    def __init__(self, message):
        super(GameEnd, self).__init__(message)