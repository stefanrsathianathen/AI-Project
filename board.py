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

	def validMoves(self, oldX, oldY):

		if  7<newX or newX<0:
			return False
		if 7<newY or newY<0:
			return False

		netMoves = 0;

		if (self.board[oldX + 1][oldY].occupiedBy == " " or
			self.board[oldX + 2][oldY].occupiedBy == " "):
			netMoves += 1;
		if (self.board[oldX - 1][oldY].occupiedBy == " " or
			self.board[oldX - 2][oldY].occupiedBy == " "):
			netMoves += 1;
		if (self.board[oldX][oldY + 1].occupiedBy == " " or
			self.board[oldX][oldY + 2].occupiedBy == " "):
			netMoves += 1;
		if (self.board[oldX][oldY - 1].occupiedBy == " " or 
			self.board[oldX][oldY - 2].occupiedBy == " "):
			netMoves += 1;

	def findNumberOfMoves(self):

		blackMoves = 0
		whiteMoves = 0

		for y in range(0, len(self.board)-1):
			for x in range(0, len(self.board[y])-1):
				netMoves = 0
				if self.board[y][x].occupiedBy == 'X' or self.board[y][x].occupiedBy == ' ':
					pass
				elif self.board[y][x].occupiedBy == '@':
					blackMoves += validMoves(x, y)
				else:
					whiteMoves += validMoves(x, y)
		print(whiteMoves)
		print(blackMoves)


	def createCell(self,x,y,occupiedBy):
		"""Creates a cell. If the cell is occupied by a @ or ) or X it will create a piece that lies on top of the cell"""
		return c.Cell(x,y,occupiedBy)

	# def destorypiece():
	# 	destorypiec

	def move(self,oldX,oldY,newX,newY):
		'''Moves piece on board'''
	 #	check if player can move (NEED VALID MOVE)
		self.board[oldY][oldX].changePiece(self.board[newY][newX])

	# def shrinkboard():
	# 	shrinkboard
