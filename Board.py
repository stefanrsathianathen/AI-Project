
class Board():

    def __init__(self):
        self.board = [['-' for _ in range(8)] for _ in range(8)]

        for square in [(0, 0), (7, 0), (7, 7), (0, 7)]:
            x, y = square
            self.board[y][x] = 'X'

        self.pieces = {"white" : 0, "black" : 0}
        self.n_shrinks = 0
        self.n_turns = 0
        self.placeBanList = [(0,0), (7,0), (0, 7), (7, 7)]

    def printBoard(self):
        for y in range(0, 8):
            for x in range (0, 8):
                print(self.board[y][x], end = " ")
            print("\n")
        print("\n")

    def placePiece(self, place, colour):

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

    def move(self, positions):
        '''Moves piece on board and check if need to elimate pieces,
		      if so eliminate them'''
        if self.isValidMove(positions):
            self.swapPieces(positions)

        pieceType = self.board[positions[1][1]][positions[1][0]]

        opponentPiece = "B" if pieceType == "W" else "W"

        self.eliminatePieces(positions[1][0], positions[1][1],
                            pieceType, opponentPiece)
        return self.board

    def swapPieces(self, positions):
        temp = self.board[positions[0][1]][positions[0][0]]
        self.board[positions[0][1]][positions[0][0]] = \
            self.board[positions[1][1]][positions[1][0]]
        self.board[positions[1][1]][positions[1][0]] = temp

    def isValidMove(self, positions):
        ''' Check if the positions are within the board size '''
        for x, y in positions:
            if x > 7 or x < 0 or y > 7 or y < 0:
                return False
            if self.board[y][x] == " ":
                return False

        ''' If a piece tries to jump over another piece '''
        if (abs(positions[1][0] - positions[0][0]) == 2 or
                abs (positions[1][1] - positions[0][1]) == 2):
            dx = int((positions[1][0] - positions[0][0])/2)
            dy = int((positions[1][1] - positions[0][1])/2)
            if self.board[positions[0][1] + dy][positions[0][0] + dx] == "W" or\
                self.board[positions[0][1] + dy][positions[0][0] + dx] == "B":
                return True
            else:
                return False

        ''' If the board is empty in the new position, return true '''
        if self.board[positions[1][1]][positions[1][0]] == "-":
            return True
        else:
            return False

    def destoryPiece(self, position):
        '''Destory the piece if it is no longer needed'''
        if (self.board[position[1]][position[0]] == "B"):
            self.pieces["black"] -= 1
        elif (self.board[position[1]][position[0]] == "W"):
            self.pieces["white"] -= 1
        self.board[position[1]][position[0]] = "-"
        try:
            self.placeBanList.remove((position[0], position[1]))
        except ValueError:
            pass

    def shrink_board(self):
        """
        Shrink the board, eliminating all pieces along the outermost layer,
        and replacing the corners.
        """
        s = self.n_shrinks # number of shrinks so far, or 's' for short
        # Remove edges
        for i in range(s, 8 - s):
            for square in [(i, s), (s, i), (i, 7-s), (7-s, i)]:
                x, y = square
                piece = self.board[y][x]
                if piece in self.pieces:
                    self.pieces[piece] -= 1
                self.board[y][x] = '-'

        # we have now shrunk the board once more!
        self.n_shrinks = s = s + 1
        case = 0
        # replace the corners (and perform corner elimination)
        for corner in [(s, s), (s, 7-s), (7-s, 7-s), (7-s, s)]:

            x, y = corner
            piece = self.board[y][x]
            if piece in self.pieces:
                self.pieces[piece] -= 1
            self.board[y][x] = 'X'
            self.eliminateCorners(corner)
            case+=1

    def eliminateCorners(self, corner):
        x, y = corner
        for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            try:
                if self.board[y+dy][x+dx] != "-" \
                and self.board[y+dy+dy][x+dx+dx] != "-" \
                and self.board[y+dy][x+dx] != self.board[y+dy+dy][x+dx+dx]:
                    self.destoryPiece((x+dx,y+dy))
            except IndexError:
                continue

    def eliminatePieces(self, x, y, pieceType, opponentPiece):
        '''Figure out if a piece needs to be eliminated
			by game rules if so eliminate the piece'''
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            try:
                if ((x + dx + dx) < 0 or (y + dy + dy) < 0):
                    continue

                if (self.board[y + dy][x + dx] == opponentPiece and
                    (self.board[y + dy + dy][x + dx + dx] == pieceType or
                    self.board[y + dy + dy][x + dx + dx] == "X")):
                    self.destoryPiece((x + dx, y + dy))

            except IndexError:
                continue

        if ((x + 1 < 8) and (x - 1 >= 0) and
			(self.board[y][x + 1] == opponentPiece or self.board[y][x + 1] == "X") and
			(self.board[y][x - 1] == opponentPiece or self.board[y][x - 1] == "X")):
            self.destoryPiece((x, y))
        elif ((y + 1 < 8) and (y - 1 >= 0) and
			(self.board[y + 1][x] == opponentPiece or self.board[y + 1][x] == "X") and
			(self.board[y - 1][x] == opponentPiece or self.board[y - 1][x] == "X")):
            self.destoryPiece((x, y))
