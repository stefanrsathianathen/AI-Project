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
        return minMax(parentNode).move

    ''' receive the opponent's action '''
    def update(self, action):
        if action != None:
            if (len(action) == 2):
                ''' Opponent placed a piece '''
                self.board.placePiece(action, self.opponentColour)
            if (len(action) > 2):
                ''' Opponent moved a piece '''
                print("This is action")
                print(action)
                print("dsf")
                self.board.swapPieces(action)

        self.board.n_turns += 1


    def gameStates(x, y):
        '''create the possible game states for current piece'''
        moves = []

        for dx, dy in [(1,0), (0,1), (-1,0), (0,-1), (2,0), (0,2), (-2,0), (0,-2)]:
            try:
                if self.board.isValidMove(((x, y), (x + dx, y + dy))):
                    tmpBoard = copy.deepcopy(self.board)
                    tmpBoard.move(((x, y), (x + dx, y + dy)))
                    moves.append(g.GameNode(tmpBoard, ((x, y), (x + dx, y + dy))))
            except IndexError:
                continue
        return moves

    def value():
        return randint(-20,60)

    def minMax(parentNode):
        for x in parentNode.children:
            minValue = float('inf')
            for u in x.children:
                if u.value < minValue:
                    minValue = u.value
            x.value = minValue
        maxValue = float("-inf")
        maxNode = None
        for l in parentNode.children:
            if l.value > maxValue:
                maxValue = l.value
                maxNode = l
        return maxNode

    def placeAPiece(self):

        ''' Checks if there is any adjacent opponent piece for our pieces
            and then places a piece in the opposite end to eliminate it '''
        for y in range(0, 8):
            for x in range(0, 8):
                if self.board.board[y][x] == self.myColour:
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        if self.board.board[y + dy][x + dx] == self. opponentColour and self.board.board[y + dy +dy][x + dx + dx] == "-" and (x + dx + dx, y + dy + dy) not in self.placeBanList:
                            self.board.placePiece((x + dx + dx, y + dy + dy), self.myColour)
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
                    if self.board.board[y+dy][x+dx] == self.opponentColour or self.board.board[y+dy][x+dx] == "X":
                        dangerPlace = True
                        break
                except IndexError:
                    continue
            if dangerPlace:
                continue

            if (x, y) not in self.board.placeBanList:
                self.board.placePiece((x, y), self.myColour)
                self.board.placeBanList.append((x, y))
                return ((x, y))
                break
