import Board as b
import gameTree as g
import copy

myBoard = b.Board()
piece = "W"

myBoard.placePiece((1,4), "white")
# myBoard.placePiece((4,3), "white")
# myBoard.placePiece((1,5), "black")
#
# for y in range(0, 8):
#     for x in range (0, 8):
#         print(myBoard.board[y][x], end = " ")
#     print("\n")
# print(myBoard.pieces)
#
# #myBoard.move(((2,5), (2,6)))
# myBoard.shrink_board()
#
# for y in range(0, 8):
#     for x in range (0, 8):
#         print(myBoard.board[y][x], end = " ")
#     print("\n")
# print(myBoard.pieces)
#
# myBoard.shrink_board()
#
# for y in range(0, 8):
#     for x in range (0, 8):
#         print(myBoard.board[y][x], end = " ")
#     print("\n")
# print(myBoard.pieces)

def gameStates(x, y):
    '''create the possible game states for current piece'''
    moves = []
    ''' Move to the right '''
    if myBoard.isValidMove(((x,y),(x+1,y))) or myBoard.isValidMove(((x,y),(x+2,y))):
        if(myBoard.board[y][x+1] != myBoard.board[y][x]):
            moves.append(g.GameNode(myBoard.swapPieces(((x,y),(x+1,y)))))
            #moves.append(g.GameNode(tmp))
        else:
            moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x+2,y)))))
    ''' Move to the left '''
    if myBoard.isValidMove(((x,y),(x-1,y))) or myBoard.isValidMove(((x,y),(x-2,y))):
        if(myBoard.board[y][x-1] != myBoard.board[y][x]):
            moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x-1,y)))))
        else:
            moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x-2,y)))))
    ''' Move down '''
    if myBoard.isValidMove(((x,y),(x,y+1))) or myBoard.isValidMove(((x,y),(x,y+2))):
        if(myBoard.board[y+1][x] != myBoard.board[y][x]):
            moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y+1)))))
        else:
            moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y+2)))))
    ''' Move up '''
    if myBoard.isValidMove(((x,y),(x,y-1))) or myBoard.isValidMove(((x,y),(x,y-2))):
        if(myBoard.board[y-1][x] != myBoard.board[y][x]):
            moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y-1)))))
        else:
           moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y-2)))))
    for l in moves:
        print(l.board)
    return moves

def main():
    myBoard = b.Board()
    piece = "W"

    myBoard.placePiece((1,4), "white")

    ''' Moving Phase '''
    parentNode = g.GameNode(myBoard)

    for x in range(0,len(myBoard.board)):
        for y in range(0,len(myBoard.board)):
            if myBoard.board[y][x] == piece:
                states = gameStates(x,y)
                for state in states:
                    parentNode.addChild(state.defineParent(parentNode))

    # for gameState in parentNode.children:
    #     print(gameState)
        # for x in range(0,len(gameState.board)):
        #     for y in range(0,len(gameState.board)):
        #         if gameState.board[y][x] != self.piece and gameState.board[y][x]:
        #             opponentStates = self.gameStates(x,y)
        #             for state in states:
        #                 gameState.addChild(state.defineParent(gameState))

main()
