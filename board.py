import Cell as c
class Board():
	"""docstring for Board"""

	board = [[],[],[],[],[],[],[],[]]
	numberofMoves = 0

	def __init__(self):
		pass


	def createBoard(self, boardInput):
		'''Loop through text input and put into board by creating cell
		then the cell will create a piece if it is occupied by a @ or O or X'''
		for y in range(0, len(boardInput)):
			for x in range(0, len(boardInput[y])):
				self.board[y].append(self.createCell(x, y, boardInput[y][x]))
		self.viewBoard()


	def viewBoard(self):
		#to view the board correctly
		for x in self.board:
			print(x)

	def validMoves(self, oldX, oldY):
		netMoves = 0;

		if (((oldX + 1 < 8) and self.board[oldY][oldX + 1].occupiedBy == " ") or
			 ((oldX + 2 < 8)  and self.board[oldY][oldX + 2].occupiedBy == " ")):
			netMoves += 1
		if (((oldX - 1 > -1) and self.board[oldY][oldX - 1].occupiedBy == " ") or
			 ((oldX - 2 > -1) and self.board[oldY][oldX - 2].occupiedBy == " ")):
			netMoves += 1
		if (((oldY + 1 < 8) and self.board[oldY + 1][oldX].occupiedBy == " ") or
			((oldY + 2 < 8) and self.board[oldY + 2][oldX].occupiedBy == " ")):
			netMoves += 1
		if (((oldY - 1 > -1) and self.board[oldY - 1][oldX].occupiedBy == " ") or
			 ((oldY - 2 > -1) and self.board[oldY - 2][oldX].occupiedBy == " ")):
			netMoves += 1
		return netMoves

	def findNumberOfMoves(self):

		blackMoves = 0
		whiteMoves = 0

		for y in range(0, len(self.board)):
			for x in range(0, len(self.board[y])):
				if (self.board[y][x].occupiedBy == 'X' or
					self.board[y][x].occupiedBy == ' '):
					pass
				elif self.board[y][x].occupiedBy == '@':
					blackMoves += self.validMoves(x, y)
				else:
					whiteMoves += self.validMoves(x, y)
		print(whiteMoves)
		print(blackMoves)


	def createCell(self, x, y, occupiedBy):
		"""Creates a cell. If the cell is occupied by a @ or ) or
			X it will create a piece that lies on top of the cell"""
		return c.Cell(x, y, occupiedBy)

	# def destorypiece():
	# 	destorypiec

	def move(self, oldX, oldY, newX, newY):
		'''Moves piece on board'''
	 #	check if player can move (NEED VALID MOVE)
		self.board[oldY][oldX].changePiece(self.board[newY][newX])
