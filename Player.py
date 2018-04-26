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
        self.piece = "B" if self.myColour == "black" else "W"

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
        ''' Shrink board if required '''
        if turns == 128 or turns == 192:
            self.board.shrinkboard()

        ''' Placing Phase '''
        if turns <= 24:
            return self.placeAPiece()

        ''' Moving Phase '''
        parentNode = g.GameNode(self.board)

        for x in range(0,len(self.board)):
            for y in range(0,len(self.board)):
                if self.board[y][x] == self.piece:
                    states = self.gameStates(x,y)
                    for state in states:
                        parentNode.addChild(state.defineParent(parentNode))

        for gameState in parentNode.children:
            for x in range(0,len(gameState.board)):
                for y in range(0,len(gameState.board)):
                    if gameState.board[y][x] != self.piece and gameState.board[y][x]:
                        opponentStates = self.gameStates(x,y)
                        for state in states:
                            gameState.addChild(state.defineParent(gameState))

    ''' receive the opponent's action '''
    def update(self, action):

        if action != None:
            if (len(action) == 1):
                ''' Opponent placed a piece '''
                self.board.placePiece(action, opponentColour)
            if (len(action) == 2):
                ''' Opponent moved a piece '''
                self.board.move(action)

        self.board.n_turns += 1


    def gameStates(self, x, y):
        '''create the possible game states for current piece'''
        moves = []
        ''' Move to the right '''
        if ((self.board.isValidMove((x, y), (x + 1, y)) or
             (self.board.isValidMove((x, y), (x + 2, y)))):
            if(self.board[y][x+1] != self.board[y][x]):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x+1,y))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x+2,y))))
        ''' Move to the left '''
        if ((self.board.isValidMove(x, y, x - 1, y)) or
             (self.board.isValidMove(x, y, x - 2, y))):
            if(self.board[y][x-1] != self.board[y][x]):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x-1,y))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x-2,y))))
        ''' Move down '''
        if ((self.board.isValidMove(x, y, x, y + 1)) or
            (self.board.isValidMove(x, y, x, y + 2))):
            if(self.board[y+1][x] != self.board[y][x]):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y+1))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y+2))))
        ''' Move up '''
        if ((self.board.isValidMove(x, y, x, y - 1)) or
             (self.board.isValidMove(x, y, x, y - 2))):
            if(self.board[y-1][x] != self.board[y][x]):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y-1))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y-2))))
        return moves

    def placeAPiece(self):

        ''' Checks if there is any adjacent opponent piece for our pieces
            and then places a piece in the opposite end to eliminate it '''
        for y in range(0, 8):
            for x in range(0, 8):
                if board.board[y][x] == self.myColour:
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        if board.board[y + dy][x + dx] == self.opponentColour \
                        and board.board[y + dy +dy][x + dx + dx] == "-" \
                        and (x + dx + dx, y + dy + dy) not in self.placeBanList:
                            board.placePiece((x + dx + dx, y + dy + dy), self.myColour)
                            self.placeBanList.append((x + dx + dx, y + dy + dy))
                            return ((x + dx + dx, y + dy + dy))

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
                return ((x, y))
                break
