import Board as b
import gameTree as g
import copy
from random import randint

class Player():

    ''' set up the player '''
    def __init__(self, colour):
        self.board = b.Board()
        self.myColour = colour
        self.opponentColour = "black" if self.myColour == "white" else "white"

        if self.myColour == "white":
            for x in range(0, 8):
                self.board.placeBanList.append((x, 6))
                self.board.placeBanList.append((x, 7))
        else:
            for x in range(0, 8):
                self.board.placeBanList.append((x, 0))
                self.board.placeBanList.append((x, 1))


    ''' decide the next action '''
    def action(self, turns):
        if turns == 128 or turns == 192:
            self.board.shrinkboard()

        if turns <= 24:
            self.placeAPiece()

        self.board.n_turns += 1

    ''' receive the opponent's action '''
    def update(self, action):

        if action != None:
            if (len(action) == 1):
                ''' place a piece '''
                self.board.placePiece(action, opponentColour)
            if (len(action) == 2):
                ''' move a piece '''
                self.board.move(action)

        self.board.n_turns += 1


    def nodes(self, x, y):
        '''Count how many valid moves a piece can make given the
            current board position and return that'''

        ''' Move to the right '''
        if ((self.board.isValidMove(x, y, x + 1, y)) or
             (self.board.isValidMove(x, y, x + 2, y))):
            g.GameNode(copy.deepcopy(self.board))
        ''' Move to the left '''
        if ((self.board.isValidMove(x, y, x - 1, y)) or
             (self.board.isValidMove(x, y, x - 2, y))):
            netMoves += 1
        ''' Move down '''
        if ((self.board.isValidMove(x, y, x, y + 1)) or
            (self.board.isValidMove(x, y, x, y + 2))):
            netMoves += 1
        ''' Move up '''
        if ((self.board.isValidMove(x, y, x, y - 1)) or
             (self.board.isValidMove(x, y, x, y - 2))):
            netMoves += 1
        return netMoves

    def placeAPiece(self):

        ''' Checks if there is any adjacent opponent piece for our pieces
            and then places a piece in the opposite end to eliminate it '''
        for y in range(0, 8):
            for x in range(0, 8):
                if board.board[y][x] == self.myColour:
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        if board.board[y + dy][x + dx] == self.opponentColour
                        and board.board[y + dy +dy][x + dx + dx] == "-"
                        and (x + dx + dx, y + dy + dy) not in self.placeBanList:
                            board.placePiece((x + dx + dx, y + dy + dy), self.myColour)
                            self.placeBanList.append((x + dx + dx, y + dy + dy))
                            return

        ''' Gets 2 random integers and places a piece if there is no
            adjacent opponent pieces '''
        while True:
            x = randint(0, 7)
            y = randint(0, 5)
            dangerPlace = False
            for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                try:
                    if board.board[y+dy][x+dx] == self.opponentColour or board.board[y+dy][x+dx] == "X":
                        dangerPlace = True
                        break
                except IndexError:
                    continue
            if dangerPlace:
                continue

            if (x, y) not in board.placeBanList:
                board.placePiece((x, y), self.myColour)
                board.placeBanList.append((x, y))
                break
