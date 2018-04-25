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

    ''' decide the next action '''
    def action(self, turns):
        if turns == 128 or turns == 192:
            self.board.shrinkboard()

        parentNode = g.GameNode(self.board)

        for x in range(0,len(self.board)):
            for y in range(0,len(self.board)):
                if self.board[y][x] = self.piece:
                    states = self.gameStates(x,y)
                    for state in states:
                        parentNode.addChild(state.defineParent(parentNode))





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


    def gameStates(self, x, y):
        '''create the possible game states for current piece'''
        moves = []

        ''' Move to the right '''
        if ((self.board.isValidMove(x, y, x + 1, y)) or
             (self.board.isValidMove(x, y, x + 2, y))):
            if(self.board[y][x+1] != self.piece):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x+1,y))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x+2,y))))
        ''' Move to the left '''
        if ((self.board.isValidMove(x, y, x - 1, y)) or
             (self.board.isValidMove(x, y, x - 2, y))):
            if(self.board[y][x-1] != self.piece):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x-1,y))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x-2,y))))
        ''' Move down '''
        if ((self.board.isValidMove(x, y, x, y + 1)) or
            (self.board.isValidMove(x, y, x, y + 2))):
            if(self.board[y+1][x] != self.piece):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y+1))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y+2))))
        ''' Move up '''
        if ((self.board.isValidMove(x, y, x, y - 1)) or
             (self.board.isValidMove(x, y, x, y - 2))):
            if(self.board[y-1][x] != self.piece):
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y-1))))
            else:
                moves.append(g.GameNode(copy.deepcopy(self.board).move((x,y),(x,y-2))))
        return moves
