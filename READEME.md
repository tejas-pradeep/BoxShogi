# BoxShogi Game
The project allows two people to play a game of boxShogi, which is a variation to mini 5x5 shogi, a classic japanese
strategy game.

The project is written is `Python 3.8`. The only pip package used is `abc` which lets me use an abstract class.

The game contains two input modes, interactive mode (specified by the flag -i) and file mode (specified by the flag -f)

### Game Modes

In interactive mode two players enter keyboard commands to play moves against each other. it can be started with this command.

```python3 boxShogi.py -i```

In file mode a specified file is read, and the game is built based on inputs form the file. The game state is shown when 
either the file moves run out or the game ends. The file must contain the following : Pieces, and it's location, lower and upper captured, and a list of moves.
It can be started by the following command,

```python3 boxShogi.py -f test_cases/<name of test case>```

### Design

The project contains object-oriented design. The following classes exist:

**Game**: The object of the game class contains the current state of the game. All game operating happened through this class.

**Board**: An object on this class is contained by the game object as an attribute. This class represents the current state of the game.
        It contains information on piece locations and available moves. This object is used to acess the game board to make moves and get information on current pieces.

**Player**: Two objects of this class are contained by the board object. This class represents a game player. The game has two player, an UPPER and a lower.
Objects of this class contain a list of active peices, list of captured pieces, and a reference to the player's drive (King).

**Piece**: This is an abstract class that represents a piece in the game. It's sub classes are `Drive, Notes, Governance, Shield, Relay, Preview`.
Objects of its sub classes contain information on the piece's location, its move list, and if it's promoted. Objects of its sub-classes are contained by the player object.

**Utils**: The file utils.py is imported by all the other classes. This file contains a few util functions like checking bounds of a location, and converting a square to its indices.

**Exceptions**: This file contains 5 custom exception that indicate different ways of the game ending. These exceptions are great to get a better understanding of what caused the game to end.

### Performance

There are some computationally expensive operations, like checking for and handling checks. But since the game is of limited size, board size of 5 and piece list of 12, these operations occur instantaneously.
Due to lack of time I was unable to implement some optimizations, like using a move hash table instead of a list, but even without these optimizations the code runs extremely smoothly.

### Score

My code has passed all the given testCases. In addition, I added in two additional testCases for pinned pieces and discovered attacks. These can be found is `custom_tests` folder.

For more information about the project prompt and game, refer to `README_Game_Info.md`