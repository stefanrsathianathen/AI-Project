import BoardC as b
import gameTree as g
import MiniMax as m
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
        self.seqeunceOfMoves = []

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
        parentState = g.GameNode(None, None, deepcopy(self.board))
        # Create the game tree of moves
        self.createTree(parentState, None, 0, 4)

        # Find the best move using Minimax algorithm
        # Method 1
        minimax = m.MiniMax(parentState)
        nextMove = minimax.minimax(parentState)
        # Method 2
        # nextMove = self.miniMax(parentState)

        self.board.n_turns += 1
        if nextMove == None:
            return None
        self.board.move(nextMove.move[0])
        self.seqeunceOfMoves.append(nextMove.move[0])
        return nextMove.move[0]

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

    def createTree(self, node, parent, depth, maxDepth):

        # Base Case/ Will return from the recursive calls only if this is true
        if (depth == maxDepth):
            node.parent = parent
            # Calculate the utilities of the last nodes
            node.value = self.score(node.board, node.move)
            return

        node.parent = parent
        # Find all possible moves
        if (depth % 2 == 0):
            # Max's turn
            moves = node.board.findMoves(self.piece)

        else:
            # Min's turn
            moves = node.board.findMoves(self.opponentPiece)

        # for each move
        for move in moves:
            # create a new node using the move and same board
            childNode = g.GameNode([move, node.board.move(move)], None, node.board)

            # Add to the children list
            node.addChild(childNode)

            # recursively call the same function on the child
            self.createTree(childNode, node, depth + 1, maxDepth)

            #undo the move before doing the next move
            node.board.move((childNode.move[0][1], childNode.move[0][0]), childNode.move[1])

        return

    def miniMax(self, parentState):
        """ Commence Minimax algorithm of the game tree """
        # Find the lowest value possible from the terminal nodes
        infinty = float('inf')
        for states in parentState.children:
            minValue = infinty
            for terminalStates in states.children:
                if terminalStates.value < minValue:
                    minValue = terminalStates.value
                    states.value = minValue

                    maxValue = -infinty
                    maxNode = None
                    # Find the maximum value possible to decide which state to move to.
                    for gameState in parentState.children:
                        if gameState.value > maxValue:
                            maxValue = gameState.value
                            maxNode = gameState
                            return maxNode

    def score(self, board, move):
        """ Determines a heuristic value given a certain board state """

        # Check if next move is a death
        value = 0
        if board.pieces[self.myColour] > board.pieces[self.opponentColour]:
            value += board.pieces[self.myColour] * board.pieces[self.opponentColour]
        else:
            value -= board.pieces[self.myColour] * board.pieces[self.opponentColour]

        if board.pieces[self.myColour] < self.board.pieces[self.myColour]:
            value = 0
            return
        elif board.pieces[self.opponentColour] < self.board.pieces[self.opponentColour]:
            value = 0
            return
        elif move in self.seqeunceOfMoves:
            value -= 10000 * (self.seqeunceOfMoves.index(move))

        for y in range(0, len(board.board)):
            for x in range(0, len(board.board)):
                if board.board[y][x] == self.piece:
                    # Control the very centre of board for longevity
                    if x < 2 or x > 5:
                        value -= x * y
                    else:
                        value += x * y
                    if y < 2 or y > 5:
                        value -= y * x
                    else:
                        value += y * x

                    movable = True
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        try:
                            # Helpful if the same pieces are next to each other
                            if board.board[y + dy][x + dx] == self.piece:
                                value += (x + dx) + (y + dy)

                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                value -= (x + dx) + (y + dy)

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
                            # You could work to eliminate this piece
                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                for dx1, dy1 in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                                    if (x + dx, y + dy) == (dx + dx1, dy + dy1):
                                        continue
                                    elif board.board[y + dy + dy1][x + dx + dx1] == self.piece:
                                        value += (x+ dx + dx1) + (y + dy + dy1)
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



    def pieceInDanger(self, x, y, dx, dy):
        """ Checks if a piece is in danger during the placing phase """

        # In order to get rid of negative indexing since its annoying
        if (x + dx) < 0 or (y + dy) < 0 or (x - dx) < 0 or (y - dy) < 0:
            return False

        # Check if the piece is in danger
        if ((self.board.board[y + dy][x + dx] == self.opponentPiece
        or self.board.board[y + dy][x + dx] == "X")
        and self.board.board[y - dy][x - dx] == "-"
        and (x - dx, y - dy) not in self.board.placeBanList):
            return True

        return False

    def eliminateDuringPlacing(self, x, y, dx, dy):
        """ Checks if we can eliminate any opponent piece
            by placing our piece next to it """

        # In order to get rid of negative indexing since its annoying
        if (x + dx + dx) < 0 or (y + dy + dy) < 0:
            return False

        # Eliminate the adjacent opponent piece if possible
        if (self.board.board[y + dy][x + dx] == self.opponentPiece
        and self.board.board[y + dy + dy][x + dx + dx] == "-"
        and (x + dx + dx, y + dy + dy) not in self.board.placeBanList):
            return True

        return False

    def placeAPiece(self):
        """ Checks if there is any adjacent opponent piece for our pieces
            and then places a piece in the opposite end to eliminate it """
        # Check if you can eliminate any opponent piece by placing your piece
        for y in range(0, 8):
            for x in range(0, 8):
                if self.board.board[y][x] == self.piece:
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
                        try:
                            # Check if piece is in danger
                            if self.pieceInDanger(x, y, dx, dy):
                                self.board.placePiece((x - dx, y - dy), self.myColour)
                                return ((x - dx, y - dy))

                            # Eliminate the adjacent opponent piece if possible
                            if self.eliminateDuringPlacing(x, y, dx, dy):
                                self.board.placePiece((x + dx + dx, y + dy + dy), self.myColour)
                                return (x + dx + dx, y + dy + dy)

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
