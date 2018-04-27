import Board as b
import gameTree as g
import copy

myBoard = b.Board()
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
    try:
        if myBoard.isValidMove(((x,y),(x+1,y))) or myBoard.isValidMove(((x,y),(x+2,y))):
            if(myBoard.board[y][x+1] != myBoard.board[y][x]):
                
                moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x+1,y,))),((x,y),(x+1,y))))

            else:
                moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x+2,y))),((x,y),(x+2,y))))

    except IndexError:
        pass

    ''' Move to the left '''
    try:
        if myBoard.isValidMove(((x,y),(x-1,y))) or myBoard.isValidMove(((x,y),(x-2,y))):
            if(myBoard.board[y][x-1] != myBoard.board[y][x]):
                moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x-1,y))),((x,y),(x-1,y))))

            else:
                moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x-2,y))),((x,y),(x-2,y))))

    except IndexError:
        pass

    ''' Move down '''

    try:
        if myBoard.isValidMove(((x,y),(x,y+1))) or myBoard.isValidMove(((x,y),(x,y+2))):
            if(myBoard.board[y+1][x] != myBoard.board[y][x]):
                moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y+1))),((x,y),(x,y+1))))

            else:
                moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y+2))),((x,y),(x+1,y+2))))

    except IndexError:
        pass


    ''' Move up '''
    try:
        if myBoard.isValidMove(((x,y),(x,y-1))) or myBoard.isValidMove(((x,y),(x,y-2))):
            if(myBoard.board[y-1][x] != myBoard.board[y][x]):
                moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y-1))),((x,y),(x,y-1))))

            else:
               moves.append(g.GameNode(copy.deepcopy(myBoard).move(((x,y),(x,y-2))),((x,y),(x,y-2))))

    except IndexError:
        pass
    # for l in moves:
    #     for y in range(0, 8):
    #         for x in range (0, 8):
    #             print(l.board[y][x], end = " ")
    #         print("\n")
    #     print("\n")

    return moves

def value():
    import random 
    random.seed(4)
    return random.randint(-2,6)

def minMax(parentNode):
    for x in parentNode.children:
        minValue = 10000143135134
        for u in x.children:
            if u.value < minValue:
                minValue = u.value
        x.value = minValue
    maxValue = -1234519583724
    maxNode = None
    for l in parentNode.children:
        if l.value > maxValue:
            maxValue = l.value
            maxNode = l
    return maxNode


def main():
    piece = "W"

    myBoard.placePiece((2,4), "white")
    myBoard.placePiece((3,5), "white")
    myBoard.placePiece((2,5), "black")
    myBoard.placePiece((6,3), "black")

    ''' Moving Phase '''
    parentNode = g.GameNode(copy.deepcopy(myBoard),None)
    

    for x in range(0,len(myBoard.board)):
        for y in range(0,len(myBoard.board)):
            if myBoard.board[y][x] == piece:
                states = gameStates(x,y)
                for state in states:
                    state.defineParent(parentNode)
                    parentNode.addChild(state)

    
    for gameState in parentNode.children:
        for x in range(0,len(gameState.board)):
            for y in range(0,len(gameState.board)):
                if gameState.board[y][x] != piece and gameState.board[y][x] != "X" and gameState.board[y][x] != "-":
                    opponentStates = gameStates(x,y)
                    for state in states:
                        state.defineParent(gameState)
                        state.value = value()
                        gameState.addChild(state)

    nextMove = minMax(parentNode)
    myBoard.printBoard()
    print(nextMove.move)


main()
