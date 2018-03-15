import Cell as c

class Board():
	"""docstring for Board"""

	board = [[],[],[],[],[],[],[],[]]
	numberofMoves = 0
	
	def __init__(self):
		pass
	
	
	def createBoard(self,boardInput):
		'''Loop through text input and put into board by creating cell
		then the cell will create a piece if it is occupied by a @ or O or X'''
		for y in range(0,len(boardInput)):
			for x in range(0,len(boardInput[y])):
				self.board[y].append(self.createCell(x,y,boardInput[y][x]))
		self.viewBoard()

	
	def viewBoard(self):
		#to view the board correctly
		for x in self.board:
			print(x)

	# def validMove():
	# 	check if valid valid validMove

	
	def createCell(self,x,y,occupiedBy):
		"""Creates a cell. If the cell is occupied by a @ or ) or X it will create a piece that lies on top of the cell"""
		return c.Cell(x,y,occupiedBy)

	# def winner():
	# 	check if winner

	# def destorypiece():
	# 	destorypiec

	def move(self,oldX,oldY,newX,newY):
		'''Moves piece on board'''
	 #	check if player can move (NEED VALID MOVE)
		self.board[oldY][oldX].changePiece(self.board[newY][newX])

	# def shrinkboard():
	# 	shrinkboard



