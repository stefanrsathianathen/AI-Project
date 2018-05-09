
class Board():

    def __init__(self):
        # Nested list for the board configuration
        self.board = [['-' for _ in range(8)] for _ in range(8)]
        # Assignning the corners
        for square in [(0, 0), (7, 0), (7, 7), (0, 7)]:
            x, y = square
            self.board[y][x] = 'X'

        self.pieces = {"white" : 0, "black" : 0}
        self.n_shrinks = 0
        self.n_turns = 0
        # Places where we can't place a piece in the placing phase
        self.placeBanList = [(0,0), (7,0), (0, 7), (7, 7)]

    def printBoard(self):
        for y in range(0, 8):
            for x in range (0, 8):
                print(self.board[y][x], end = " ")
            print("\n")
        print("\n")

    def placePiece(self, place, colour):
        """ Places the specified colour piece on the board and eliminates
            required pieces while adding the new position to placeBanList """
        x, y = place
        if colour == "white":
            self.board[y][x] = "W"
            self.placeBanList.append((x, y))
            self.pieces["white"] += 1
            self.eliminatePieces(x, y, "W", "B")
        elif colour == "black":
            self.board[y][x] = "B"
            self.placeBanList.append((x, y))
            self.pieces["black"] += 1
            self.eliminatePieces(x, y, "B", "W")

    def move(self, positions, eliminatedPieces = None):
        """ Moves a piece on board after checking if its a valid move
            and checks if any pieces are eliminated. If the eliminatedPieces
            parameter is not None, it essentially means its an undo move and it
            is used to bring the pieces from the previous move. """

        if self.isValidMove(positions):
            self.swapPieces(positions)

        # If it is an undoMove
        if eliminatedPieces != None:
            for pieces in eliminatedPieces:
                self.board[pieces[0][1]][pieces[0][0]] = pieces[1]
            return

        pieceType = self.board[positions[1][1]][positions[1][0]]

        opponentPiece = "B" if pieceType == "W" else "W"

        return (self.eliminatePieces(positions[1][0], positions[1][1],
                            pieceType, opponentPiece))

    def swapPieces(self, positions):
        """ Swaps the position of two pieces on the specified positions """
        temp = self.board[positions[0][1]][positions[0][0]]
        self.board[positions[0][1]][positions[0][0]] = self.board[positions[1][1]][positions[1][0]]
        self.board[positions[1][1]][positions[1][0]] = temp

    def isValidMove(self, positions):
        """ Checks if the specified move in the positions parameter maintains
            all the game rules """

        # Check if the positions are within the board size
        for x, y in positions:
            if x > 7 or x < 0 or y > 7 or y < 0:
                return False
            if self.board[y][x] == " ":
                return False

        # If a piece tries to jump over another piece
        if (abs(positions[1][0] - positions[0][0]) == 2 or
                abs (positions[1][1] - positions[0][1]) == 2):
            dx = int((positions[1][0] - positions[0][0])/2)
            dy = int((positions[1][1] - positions[0][1])/2)
            if (self.board[positions[0][1] + dy][positions[0][0] + dx] != "W" and
            self.board[positions[0][1] + dy][positions[0][0] + dx] != "B"):
                return False

        # If the board is empty in the new position, return true
        if self.board[positions[1][1]][positions[1][0]] == "-":
            return True
        else:
            return False

    def destoryPiece(self, position):
        """ Destory the piece after reducing the piece count
            if it gets eliminated """

        if (self.board[position[1]][position[0]] == "B"):
            self.pieces["black"] -= 1
        elif (self.board[position[1]][position[0]] == "W"):
            self.pieces["white"] -= 1
        self.board[position[1]][position[0]] = "-"
        # Remove the position from the placeBanList since it is empty now
        try:
            self.placeBanList.remove((position[0], position[1]))
        except ValueError:
            pass

    def shrink_board(self):
        """ Shrink the board, eliminating all pieces along the outermost layer,
            and replacing the corners. Taken from the referee.py file with some
            edits to fit our model. """

        s = self.n_shrinks # number of shrinks so far, or 's' for short
        # Remove edges
        for i in range(s, 8 - s):
            for square in [(i, s), (s, i), (i, 7-s), (7-s, i)]:
                x, y = square
                piece = self.board[y][x]
                if piece in self.pieces:
                    self.pieces[piece] -= 1
                self.board[y][x] = ' '

        # we have now shrunk the board once more!
        self.n_shrinks = s = s + 1

        # replace the corners (and perform corner elimination)
        for corner in [(s, s), (s, 7-s), (7-s, 7-s), (7-s, s)]:

            x, y = corner
            piece = self.board[y][x]

            if piece == "W":
                self.pieces["white"] -= 1
            elif piece == "B":
                self.pieces["black"] -= 1
            self.board[y][x] = 'X'
            self.eliminateCorners(corner)

    def eliminateCorners(self, corner):
        """ Eliminates the required pieces near the new corners after the Board
            shrinks. """

        x, y = corner
        for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            if (x + dx + dx) < 0 or (y + dy + dy) < 0:
                continue

            try:
                if (self.board[y+dy][x+dx] != "-"
                and self.board[y+dy+dy][x+dx+dx] != "-"
                and self.board[y+dy][x+dx] != self.board[y+dy+dy][x+dx+dx]):
                    self.destoryPiece((x+dx,y+dy))
            except IndexError:
                continue

    def eliminatePieces(self, x, y, pieceType, opponentPiece):
        """ Eliminates the required pieces around the specified position.
            The pieceType and opponentPiece parameters are used to give the
            upper hand to the pieceType. """
        # Required if we want to undo the move later.
        eliminatedPieces = []

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            try:
                if ((x + dx + dx) < 0 or (y + dy + dy) < 0):
                    continue

                if (self.board[y + dy][x + dx] == opponentPiece and
                (self.board[y + dy + dy][x + dx + dx] == pieceType or
                self.board[y + dy + dy][x + dx + dx] == "X")):
                    eliminatedPieces.append([(x + dx, y + dy), opponentPiece])
                    self.destoryPiece((x + dx, y + dy))


            except IndexError:
                continue

        # Self elimination cases(horizontally and vertically)
        if ((x + 1 < 8) and (x - 1 >= 0) and
		(self.board[y][x + 1] == opponentPiece or self.board[y][x + 1] == "X") and
		(self.board[y][x - 1] == opponentPiece or self.board[y][x - 1] == "X")):
            eliminatedPieces.append([(x, y), pieceType])
            self.destoryPiece((x, y))
        elif ((y + 1 < 8) and (y - 1 >= 0) and
		(self.board[y + 1][x] == opponentPiece or self.board[y + 1][x] == "X") and
		(self.board[y - 1][x] == opponentPiece or self.board[y - 1][x] == "X")):
            eliminatedPieces.append([(x, y), pieceType])
            self.destoryPiece((x, y))

        # The return value is only assigned if we want to undo the move later
        return eliminatedPieces

    def notSafe(self, x, y, pieceType, opponentPiece):
        """ Figure out if a piece needs to be eliminated
            by game rules if so return True """

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            try:
                if ((x + dx + dx) < 0 or (y + dy + dy) < 0):
                    continue

                if (self.board[y + dy][x + dx] == opponentPiece and
                (self.board[y + dy + dy][x + dx + dx] == pieceType or
                self.board[y + dy + dy][x + dx + dx] == "X")):
                    return True

            except IndexError:
                continue

        if ((x + 1 < 8) and (x - 1 >= 0) and
        (self.board[y][x + 1] == opponentPiece or self.board[y][x + 1] == "X") and
        (self.board[y][x - 1] == opponentPiece or self.board[y][x - 1] == "X")):
            return True
        elif ((y + 1 < 8) and (y - 1 >= 0) and
        (self.board[y + 1][x] == opponentPiece or self.board[y + 1][x] == "X") and
        (self.board[y - 1][x] == opponentPiece or self.board[y - 1][x] == "X")):
           return True
        return False
