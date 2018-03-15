import Board as b



#creates the board
board = b.Board()

#reads all the input 
no_of_lines = 8
lines = [[]]*no_of_lines
for i in range(no_of_lines):
    lines[i]=list(input().replace(' ', ''))

#populates the board with the pieces
board.createBoard(lines)
board.move(1,6,1,7)
print("\n")
print("\n")
print("moved:" )
board.viewBoard()