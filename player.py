from piece import Drive
class Player:
    """
    Class representing a player object.

    Attributes:
        type: String representing the player type, lower or UPPER
        pieces: List containing all active pieces of the player.
        captured: List containing all pieces captured by the player.
        drive: Drive piece object of the current player.

    Class also has getters, setters, add and remove methods fro its various attributes as needed.
    """

    def __init__(self, type):
        self.type = type
        self.pieces = list()
        self.captured = list()
        self.drive = Drive(type, (0, 0))
    def getPieces(self):
        return self.pieces
    def setPieces(self, pieces):
        self.pieces = pieces
    def addPiece(self, piece):
        self.pieces.append(piece)
    def removePiece(self, piece):
        self.pieces.remove(piece)
    def getCaptured(self):
        return self.captured
    def setCaptured(self, captured_list):
        self.captured = captured_list
    def addCapture(self, capture):
        self.captured.append(capture)
    def removeCapture(self, capture):
        self.captured.remove(capture)
    def getType(self):
        return self.type
    def getDrive(self):
        return self.drive