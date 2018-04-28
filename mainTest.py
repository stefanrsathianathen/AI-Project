import Board as b
import gameTree as g
import copy
from random import randint

myBoard = b.Board()

def gameStates(x, y, rootBoard):
    '''create the possible game states for current piece'''
    moves = []

    for dx, dy in [(1,0), (0,1), (-1,0), (0,-1), (2,0), (0,2), (-2,0), (0,-2)]:
        try:
            if rootBoard.isValidMove(((x, y), (x + dx, y + dy))):
                tmpBoard = copy.deepcopy(rootBoard)
                tmpBoard.move(((x, y), (x + dx, y + dy)))
                moves.append(g.GameNode(tmpBoard, ((x, y), (x + dx, y + dy))))
        except IndexError:
            #pass
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


def main():
    piece = "W"
    opponentPiece = "B"

    ''' place 12 pieces for both '''
    for i in range(0, 12):
        while True:
            x, y = randint(0,7), randint(0,7)
            if (x, y) not in myBoard.placeBanList:
                myBoard.placePiece((x, y), "white")
                break
        while True:
            x, y = randint(0,7), randint(0,7)
            if (x, y) not in myBoard.placeBanList:
                myBoard.placePiece((x, y), "black")
                break

    ''' Moving Phase '''
    parentNode = g.GameNode(copy.deepcopy(myBoard),None)


    lvl2node = 0
    lvl3node = 0
    for x in range(0,len(myBoard.board)):
        for y in range(0,len(myBoard.board)):
            if myBoard.board[y][x] == piece:
                states = gameStates(x, y, myBoard)
                for state in states:
                    state.defineParent(parentNode)
                    parentNode.addChild(state)
                    #state.board.printBoard()
                    #print("\n", state.move)
                    lvl2node += 1


    for gameState in parentNode.children:
        for x in range(0, 8):
            for y in range(0, 8):
                if gameState.board.board[y][x] == opponentPiece:
                    opponentStates = gameStates(x,y, gameState.board)
                    for state in opponentStates:
                        state.defineParent(gameState)
                        state.value = value()
                        gameState.addChild(state)
                        #state.board.printBoard()
                        lvl3node += 1

    nextMove = minMax(parentNode)
    myBoard.printBoard()
    print(nextMove.move, lvl2node, lvl3node)

    # minMax = m.MiniMax(parentNode)
    # minMax.minimax(parentNode)


main()
