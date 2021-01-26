class MoveException(Exception):
    def __init__(self, message):
        super(MoveException, self).__init__(message)

class WrongPlayerException(Exception):
    def __init__(self, message):
        super(WrongPlayerException, self).__init__(message)

class PositionOutofBoundsException(Exception):
    def __init__(self, message):
        super(PositionOutofBoundsException, self).__init__(message)