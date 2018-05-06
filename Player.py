import Board as b
import gameTree as g
from copy import deepcopy
from random import randint
from collections import Counter

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
        if (self.board.n_turns == 152 or self.board.n_turns == 153 or
        self.board.n_turns == 216 or self.board.n_turns == 217):
            self.board.shrink_board()
            # self.board.printBoard()

        ''' Placing Phase '''
        if self.myColour == "white" and self.board.n_turns < 23:
            next = self.placeAPiece()
            self.board.n_turns += 1
            # self.board.printBoard()
            return next
        elif self.myColour == "black" and self.board.n_turns < 24:
            next = self.placeAPiece()
            self.board.n_turns += 1
            # self.board.printBoard()
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
                            state.value = self.score(state.board)
                            state.defineParent(gameState)
                            gameState.addChild(state)

        nextMove = self.minMax(parentNode)
        self.board.n_turns += 1
        self.board.move(nextMove.move)
        # self.board.printBoard()
        return nextMove.move

    ''' receive the opponent's action '''
    def update(self, action):
        if action != None:

            if (type(action[0]) == int):
                ''' Opponent placed a piece '''
                self.board.placePiece(action, self.opponentColour)
                # self.board.printBoard()
            else:
                ''' Opponent moved a piece '''
                self.board.move(action)
                # self.board.printBoard()

        self.board.n_turns += 1


    def gameStates(self, x, y, rootBoard):
        '''create the possible game states for current piece'''
        moves = []

        for dx, dy in [(1,0), (0,1), (-1,0), (0,-1), (2,0), (0,2), (-2,0), (0,-2)]:
            try:
                if x + dx > 0 and y + dy > 0:
                    if rootBoard.isValidMove(((x, y), (x + dx, y + dy))) and rootBoard.board[y + dy][x + dx] == "-":
                        tmpBoard = deepcopy(rootBoard)
                        tmpBoard.move(((x, y), (x + dx, y + dy)))
                        moves.append(g.GameNode(tmpBoard, ((x, y), (x + dx, y + dy))))
                else:
                    continue
            except IndexError:
                continue
        return moves

    def score(self,board):
        #check if next move is a death
        value = 0
        if board.board.count(self.piece) > board.board.count(self.opponentPiece):
            value += board.board.count(self.piece)*board.board.count(self.opponentPiece)
        else:
            value -= board.board.count(self.piece)*board.board.count(self.opponentPiece)
        for x in range(0,len(board.board)):
            for y in range(0,len(board.board)):
                if board.board[y][x] == self.piece:
                    #control the very centre of board for longivity
                    if x < 2 or x > 5:
                        value -= 100 * x*y
                    else:
                        value += 10 * x*y
                    if y < 2 or y > 5:
                        value -= 100 * y*x
                    else:
                        value += 10 * y*x

                    movable = True
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        #check if piece may be elimated
                        try:
                            if board.notSafe(x+dx,y+dx,self.piece, self.opponentPiece):
                                    value -= 100 * (x + dx) + 50 * (y + dy)
                            else:
                                    value += 10 * (x + dx) + 5 * (y + dy)
                        except IndexError:
                            pass
                        #not helpful if the same pieces are right next to each other
                        try:
                            if board.board[y + dy][x + dx] == self.piece:
                                value -= 100 * (x + dx) + 50 * (y + dy)
                        except IndexError:
                            pass
                        #Its good to have control of cells in corners for easy kills
                        try:
                            if board.board[y + dy][x + dx] == "X":
                                value += 10 * (x + dx) + 5 * (y + dy)
                        except IndexError:
                            pass
                        # Want to move closer to other pieces so you can eliminate them
                        try:
                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                value += 10 * (x + dx) + 5 * (y + dy)
                                try:
                                    if board.board[y + (dy*2)][x + (dx*2)] == self.piece:
                                        value += 10 * (x + dx) + 5 * (y + dy)
                                except IndexError:
                                    pass

                        except IndexError:
                            pass
                        #its good if a piece has a valid move after moving
                        try:
                            if not board.isValidMove(((x, y), (x + dx, y + dy))):
                                movable = False
                        except IndexError:
                            value -= 100 * (x*y)
                    if movable:
                        value += 10 * (x*y)
                    else:
                        value -= 100 * (x*y)
                    #check diagonals
                    for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        try:
                            # you dont want pieces to close togther
                            if board.board[y + dy][x + dx] == self.piece:
                                value -= 100 * (x + dx) + 50 * (y + dy)
                        except IndexError:
                            value -= 100 * (x + dx) + 50 * (y + dy)
                        try:
                            # you could work to elimate this piece
                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                for dx1, dy1 in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                                    if (x+dx,y+dy) == (dx+dx1,dy+dy1):
                                        continue
                                    if board.board[dy+dy1][dx+dx1] == self.piece:
                                        value += 10 * (dx + dx1) + 5 * (dy + dy1)
                                    elif board.board[dy+dy1][dx+dx1] == self.opponentPiece:
                                        value -= 100 * (dx + dx1) + 50 * (dy + dy1)
                        except IndexError:
                            value -= 100 * (x + dx) + 50 * (y + dy)
                    for dx, dy in [(2, 0), (0, 2), (0, -2), (-2, 0)]:
                        #looking for close
                        try:
                            if board.board[y + dy][x + dx] == self.piece:
                                value += 10 * (x + dx) + 5 * (y + dy)
                        except IndexError:
                            value += 10 * (x + dx) + 5 * (y + dy)
        return value


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
                            if (x + dx + dx) < 0 or (y + dy + dy) < 0:
                                continue

                            if self.board.board[y + dy][x + dx] == self.opponentPiece and self.board.board[y + dy +dy][x + dx + dx] == "-" and (x + dx + dx, y + dy + dy) not in self.board.placeBanList:
                                if x + dx + dx > 0 and y + dy + dy > 0:
                                    self.board.placePiece((x + dx + dx, y + dy + dy), self.myColour)
                                    return (x + dx + dx, y + dy + dy)
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
                if (x + dx) < 0 or (y + dy) < 0:
                    continue

                try:
                    if self.board.board[y+dy][x+dx] == self.opponentPiece or self.board.board[y+dy][x+dx] == "X":
                        dangerPlace = True
                        break
                except IndexError:
                    continue
            if dangerPlace:
                continue

            if (x, y) not in self.board.placeBanList:
                self.board.placePiece((x, y), self.myColour)
                return ((x, y))
