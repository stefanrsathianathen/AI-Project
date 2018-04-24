import Board as b
import gameTree as g
import copy
class Player():

    ''' set up the player '''
    def __init__(self, colour):
        self.board = b.Board()
        self.myColour = colour
        self.opponentColour = "black" if self.myColour == "white" else "white"


    ''' decide the next action '''
    def action(self, turns):
        if turns == 128 or turns == 192:
            self.board.shrinkboard()
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