class Player:

    def __init__(self, type_player):
        self.type = type_player
        self.pieces = None
        self.captured_pieces = None
        self.check = False
        self.checkmate = False
        self.check_moves = None
        self.escape_moves = None
        self.drop_pieces = None

    def getType(self):
        return self.type

    def getPieces(self):
        return self.pieces

    def getCaptured(self):
        return self.captured_pieces

    def isCheck(self):
        return self.check

    def isCheckmate(self):
        return self.checkmate

    def getCheckMoves(self):
        return self.check_moves

    def getExcapeMoves(self):
        return self.escape_moves

    def getDropPieces(self):
        return self.drop_pieces

    def setPieces(self, pieces):
        self.pieces = pieces

    def updatePieceLocation(self, piece, location):
        self.pieces[piece] = location

    def updateCaptured(self, captured):
        self.captured_pieces.append(captured)

    def updateCheck(self, is_check):
        self.check = is_check

