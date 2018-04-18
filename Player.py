import Board as b

class Player():

    ''' set up the player '''
    def __init__(self, colour):
        self.board = b.Board()
        self.myColour = colour
        self.opponentColour = "black" if self.myColour == "white" else "white"


    ''' decide the next action '''
    def action(self, turns):
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
