import Board as b
import gameTree as g
from copy import deepcopy
from random import randint

class Player():

    ''' set up the player '''
    def __init__(self, colour):
        self.board = b.Board()
        self.myColour = colour
        self.opponentColour = "black" if self.myColour == "white" else "white"
        self.piece = "B" if self.myColour == "black" else "W"
        self.opponentPiece = "W" if self.piece == "B" else "B"

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
        if self.myColour == "white" and self.board.n_turns < 23:
            next = self.placeAPiece()
            self.board.n_turns += 1
            return next
        elif self.myColour == "black" and self.board.n_turns < 24:
            next = self.placeAPiece()
            self.board.n_turns += 1
            return next

        ''' Moving Phase '''
        parentNode = g.GameNode(deepcopy(self.board), None)

        for y in range(0,len(self.board.board)):
            for x in range(0,len(self.board.board[y])):
                if self.board.board[y][x] == self.piece:
                    states = self.gameStates(x, y, self.board)
                    for state in states:
                        state.defineParent(parentNode)
                        parentNode.addChild(state)

        for gameState in parentNode.children:
            for y in range(0, len(gameState.board.board)):
                for x in range(0, len(gameState.board.board[y])):
                    if gameState.board.board[y][x] == self.opponentPiece:
                        opponentStates = self.gameStates(x, y, gameState.board)
                        for state in opponentStates:
                            state.value = self.value()
                            state.defineParent(gameState)
                            gameState.addChild(state)
        nextMove = self.minMax(parentNode)
        self.board.n_turns += 1
        #print(move)
        return nextMove.move

    ''' receive the opponent's action '''
    def update(self, action):
        if action != None:

            if (type(action[0]) == int):
                ''' Opponent placed a piece '''
                self.board.placePiece(action, self.opponentColour)
                self.board.placeBanList.append(action)
            else:
                ''' Opponent moved a piece '''
                self.board.swapPieces(action)

        self.board.n_turns += 1


    def gameStates(self, x, y, rootBoard):
        '''create the possible game states for current piece'''
        moves = []

        for dx, dy in [(1,0), (0,1), (-1,0), (0,-1), (2,0), (0,2), (-2,0), (0,-2)]:
            try:
                if rootBoard.isValidMove(((x, y), (x + dx, y + dy))):
                    tmpBoard = deepcopy(rootBoard)
                    tmpBoard.move(((x, y), (x + dx, y + dy)))
                    moves.append(g.GameNode(tmpBoard, ((x, y), (x + dx, y + dy))))
            except IndexError:
                continue
        return moves

    def value(self):
        return randint(-20,60)

    def minMax(self, parentNode):
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
                if self.board.board[y][x] == self.piece:
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        try:
                            if self.board.board[y + dy][x + dx] == self.opponentPiece and self.board.board[y + dy +dy][x + dx + dx] == "-" and (x + dx + dx, y + dy + dy) not in self.board.placeBanList:
                                self.board.placePiece((x + dx + dx, y + dy + dy), self.myColour)
                                if x + dx + dx > 0 and y + dy + dy > 0:
                                    return ((x + dx + dx, y + dy + dy))
                                else:
                                    continue
                        except IndexError:
                            continue

        ''' Gets 2 random integers and places a piece if there is no
            adjacent opponent pieces '''
        while True:
            x = randint(0, 7)
            if self.myColour == "white":
                y = randint(0, 5)
            else:
                y = randint(2, 7)

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
                return ((x, y))
