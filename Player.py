import BoardC as b
import gameTree as g
from copy import deepcopy
from random import randint
from collections import Counter

class Player():

    def __init__(self, colour):
        """ Set up the player """
        # Our own board represaentation
        self.board = b.Board()
        # Colour and Piece representations
        self.myColour = colour
        self.opponentColour = "black" if self.myColour == "white" else "white"
        self.piece = "B" if self.myColour == "black" else "W"
        self.opponentPiece = "W" if self.piece == "B" else "B"

        # Adding positions to the placeBanList according to the game rules
        if self.myColour == "white":
            for x in range(0, 8):
                self.board.placeBanList.append((x, 6))
                self.board.placeBanList.append((x, 7))
        else:
            for x in range(0, 8):
                self.board.placeBanList.append((x, 0))
                self.board.placeBanList.append((x, 1))

    def action(self, turns):
        """ Decides the next action """

        # Shrink board if required
        if (turns == 128 or turns == 129 or turns == 192 or turns == 193):
            self.board.shrink_board()

        # Placing Phase
        if self.myColour == "white" and self.board.n_turns < 23:
            self.board.n_turns += 1
            return self.placeAPiece()
        elif self.myColour == "black" and self.board.n_turns < 24:
            self.board.n_turns += 1
            return self.placeAPiece()

        # Moving Phase
        parentNode = g.GameNode(deepcopy(self.board), None)
        # Create the game tree
        self.createTree(parentNode)
        # Find the best move using Minimax algorithm
        nextMove = self.miniMax(parentNode)
        self.board.n_turns += 1
        if nextMove == None:
            return (None)
        self.board.move(nextMove.move)
        self.lastMove = nextMove.move
        return nextMove.move

    def update(self, action):
        """ Receive the opponent's move and update our own board """

        if action != None:
            # Opponent placed a piece
            if (type(action[0]) == int):
                self.board.placePiece(action, self.opponentColour)
            # Opponent moved a piece
            else:
                self.board.move(action)

        self.board.n_turns += 1

    def createTree(self,parentNode):
        for y in range(0,len(parentNode.board.board)):
                for x in range(0,len(parentNode.board.board[y])):
                    if self.board.board[y][x] == self.piece:
                        states = self.gameStates(x,y, parentNode.board)
                        for state in states:
                            state.defineParent(parentNode)
                            parentNode.addChild(state)

        for gameState in parentNode.children:
            for y in range(0, len(gameState.board.board)):
                for x in range(0, len(gameState.board.board[y])):
                    if gameState.board.board[y][x] == self.opponentPiece:
                        opponentStates = self.gameStates(x, y, gameState.board)
                        for state in opponentStates:
                            if state == None:
                                continue
                            state.value = self.score(state.board)
                            state.defineParent(gameState)
                            gameState.addChild(state)


    def gameStates(self, x, y, rootBoard):
        """ Create the possible game states for current piece """
        moves = []

        for dx, dy in [(1,0), (0,1), (-1,0), (0,-1), (2,0), (0,2), (-2,0), (0,-2)]:
            try:
                if x + dx  > 0 and y + dy  > 0:
                    if rootBoard.isValidMove(((x, y), (x + dx, y + dy))):
                        tmpBoard = deepcopy(rootBoard)
                        tmpBoard.move(((x, y), (x + dx, y + dy)))
                        moves.append(g.GameNode(tmpBoard, ((x, y), (x + dx, y + dy))))
                else:
                    continue
            except IndexError:
                continue
        return moves

    def score(self, board):
        """ Determines a heuristic value given a certain board state """

        # Check if next move is a death
        value = 0
        if board.board.count(self.piece) > board.board.count(self.opponentPiece):
            value += board.board.count(self.piece)**board.board.count(self.opponentPiece)
        else:
            value -= board.board.count(self.piece)**board.board.count(self.opponentPiece)
        for x in range(0,len(board.board)):
            for y in range(0,len(board.board)):
                if board.board[y][x] == self.piece:
                    # Control the very centre of board for longevity
                    if x < 2 or x > 5:
                        value -= 100 * x**y
                    else:
                        value += 10 * x**y
                    if y < 2 or y > 5:
                        value -= 100 * y**x
                    else:
                        value += 10 * y**x

                    movable = True
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        try:
                            # Check if piece can get eliminated
                            if board.notSafe(x + dx, y + dx, self.piece, self.opponentPiece):
                                    value -= 10000 * (x + dx) + 50 * (y + dy)
                            else:
                                    value += 10 * (x + dx) + 5 * (y + dy)

                            # Not helpful if the same pieces are next to each other
                            if board.board[y + dy][x + dx] == self.piece:
                                value += 10 * (x + dx) + 50 * (y + dy)

                            # Good to have control of cells in corners for easy kills
                            if board.board[y + dy][x + dx] == "X":
                                value += 10 * (x + dx) + 5 * (y + dy)

                            # Want to move closer to other pieces so you can eliminate them
                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                value += 10 * (x + dx) + 5 * (y + dy)
                                try:
                                    if board.board[y + (dy * 2)][x + (dx * 2)] == self.piece:
                                        value += 10 * (x + dx) + 5 * (y + dy)
                                except IndexError:
                                    pass
                        except IndexError:
                            pass

                        # Good if a piece has a valid move after moving
                        try:
                            if not board.isValidMove(((x, y), (x + dx, y + dy))):
                                movable = False
                        except IndexError:
                            value -= 100 * (x*y)
                    if movable:
                        value += 10 * (x*y)
                    else:
                        value -= 100 * (x*y)

                    # Check diagonals
                    for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        try:
                            # You dont want pieces too close together
                            if board.board[y + dy][x + dx] == self.piece:
                                value -= 100 * (x + dx) + 50 * (y + dy)
                            # You could work to eliminate this piece
                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                for dx1, dy1 in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                                    if (x + dx, y + dy) == (dx + dx1, dy + dy1):
                                        continue
                                    if board.board[dy + dy1][dx + dx1] == self.piece:
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


    def miniMax(self, parentNode):
        """ Commence Minimax algorithm of the game tree """
        # Find the lowest value possible from the terminal nodes
        for states in parentNode.children:
            minValue = float('inf')
            for terminalStates in states.children:
                if terminalStates.value < minValue:
                    minValue = terminalStates.value
            states.value = minValue

        maxValue = float('-inf')
        maxNode = None
        # Find the maximum value possible to decide which state to move to.
        for gameState in parentNode.children:
            if gameState.value > maxValue:
                maxValue = gameState.value
                maxNode = gameState
        return maxNode

    def placeAPiece(self):
        """ Checks if there is any adjacent opponent piece for our pieces
            and then places a piece in the opposite end to eliminate it """
        # Check if you can eliminate any opponent piece by placing your piece
        for y in range(0, 8):
            for x in range(0, 8):
                if self.board.board[y][x] == self.piece:
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        try:
                            if (x + dx + dx) < 0 or (y + dy + dy) < 0:
                                continue

                            if (self.board.board[y + dy][x + dx] == self.opponentPiece
                            and self.board.board[y + dy +dy][x + dx + dx] == "-"
                            and (x + dx + dx, y + dy + dy) not in self.board.placeBanList):
                                if x + dx + dx > 0 and y + dy + dy > 0:
                                    self.board.placePiece((x + dx + dx, y + dy + dy), self.myColour)
                                    return (x + dx + dx, y + dy + dy)
                                else:
                                    continue
                        except IndexError:
                            continue

        # Tries to place a piece on the middle positions of the board first
        counter = 0
        while True:
            lowerBound = 3
            upperBound = 4
            # The range for placing slowly grows outwards
            # if it cannot find a place at first within a few tries
            if counter > 5 and counter < 15:
                lowerBound = 2
                upperBound = 5
            elif counter > 15 and counter < 50:
                lowerBound = 1
                upperBound = 6
            elif counter > 50:
                lowerBound = 0
                upperBound = 7

            x = randint(lowerBound, upperBound)
            y = randint(lowerBound, upperBound)
            print(x, y)

            counter += 1
            # Checks if the piece will get eliminated next turn if we
            # place a piece in the generated position
            dangerPlace = False
            for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                # In order to get rid of negative indexing since its annoying
                if (x + dx) < 0 or (y + dy) < 0:
                    continue

                try:
                    if ((self.board.board[y+dy][x+dx] == self.opponentPiece or
                    self.board.board[y+dy][x+dx] == "X") and
                    self.board.board[y-dy][x-dx] == "-"):
                        dangerPlace = True
                        break
                except IndexError:
                    continue
            if dangerPlace:
                continue
            # Place the piece if the game rules allow it and then return
            if (x, y) not in self.board.placeBanList:
                self.board.placePiece((x, y), self.myColour)
                return ((x, y))
