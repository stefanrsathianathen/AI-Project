import Board as b

myBoard = b.Board()

myBoard.placePiece((1,4), "white")
myBoard.placePiece((4,3), "white")
myBoard.placePiece((1,5), "black")

for y in range(0, 8):
    for x in range (0, 8):
        print(myBoard.board[y][x], end = " ")
    print("\n")
print(myBoard.pieces)

#myBoard.move(((2,5), (2,6)))
myBoard.shrink_board()

for y in range(0, 8):
    for x in range (0, 8):
        print(myBoard.board[y][x], end = " ")
    print("\n")
print(myBoard.pieces)
