
class Board():

    def __init__(self):
        self.board = [['-' for _ in range(8)] for _ in range(8)]
        for square in [(0, 0), (7, 0), (7, 7), (0, 7)]:
            x, y = square
            self.board[y][x] = 'X'

        self.pieces = {"W" : 0, "B" : 0}
        self.n_shrinks = 0
        self.n_turns = 0

    def placePiece(self, place, colour):

        x, y = place
        if colour == "white":
            self.board[y][x] = "W"
            self.pieces["W"] += 1
        elif colour == "black":
            self.board[y][x] = "B"
            self.pieces["B"] += 1

    def move(self, positions):
        '''Moves piece on board and check if need to elimate pieces,
		      if so eliminate them'''
        if self.isValidMove(positions):
            self.swapPieces(positions)

        pieceType = self.board[positions[1][1]][positions[1][0]]

        if pieceType == "W":
            opponentPiece = "B"
        else:
            opponentPiece = "W"

        self.eliminatePieces(positions[1][0], positions[1][1],
                            pieceType, opponentPiece)

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

        ''' If a piece tries to jump over another piece '''
        if (abs(positions[1][0] - positions[0][0]) > 2 or
                abs (positions[1][1] - positions[0][1]) > 2):
            return False

        ''' If the board is empty in the new position, return true '''
        if self.board[positions[1][1]][positions[1][0]] == "-":
            return True
        else:
            return False

    def destoryPiece(self, position):
        '''Destory the piece if it is no longer needed'''
        if (self.board[position[1]][position[0]] == "B"):
            self.pieces["B"] -= 1
        elif (self.board[position[1]][position[0]] == "W"):
            self.pieces["W"] -= 1
        self.board[position[1]][position[0]] = "-"

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
                self.board[y][x] = ' '

        # we have now shrunk the board once more!
        self.n_shrinks = s = s + 1

        # replace the corners (and perform corner elimination)
        for corner in [(s, s), (s, 7-s), (7-s, 7-s), (7-s, s)]:
            x, y = corner
            piece = self.board[y][x]
            if piece in self.pieces:
                self.pieces[piece] -= 1
            self.board[y][x] = 'X'
            #self.eliminatePieces(corner[0], corner[1],)

    def eliminatePieces(self, x, y, pieceType, opponentPiece):
        '''Figure out if a piece needs to be eliminated
			by game rules if so eliminate the piece'''
        if ((x + 2 < 8) and self.board[y][x + 1] == opponentPiece and
	        (self.board[y][x + 2] == pieceType or self.board[y][x + 2] == "X")):
            self.destoryPiece((x + 1, y))
        elif ((x - 2 >= 0) and self.board[y][x - 1] == opponentPiece
			and (self.board[y][x - 2] == pieceType or
			self.board[y][x -2] == "X")):
            self.destoryPiece((x - 1, y))
        elif ((y + 2 < 8) and self.board[y + 1][x] == opponentPiece
			and (self.board[y + 2][x] == pieceType or
			self.board[y + 2][x] == "X")):
            self.destoryPiece((x, y + 1))
        elif ((y - 2 >= 0) and self.board[y - 1][x] == opponentPiece
			and (self.board[y - 2][x] == pieceType or
			self.board[y - 2][x] == "X")):
            self.destoryPiece((x, y - 1))
        elif ((x + 1 < 8) and (x - 1 >= 0) and
			self.board[y][x + 1] == opponentPiece and
			self.board[y][x - 1] == opponentPiece):
            self.destoryPiece((x, y))
        elif ((y + 1 < 8) and (y - 1 >= 0) and
			self.board[y + 1][x] == opponentPiece and
			self.board[y - 1][x] == opponentPiece):
            self.destoryPiece((x, y))
