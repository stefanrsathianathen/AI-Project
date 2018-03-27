import Cell as c
class Board():
	"""docstring for Board"""

	board = [[],[],[],[],[],[],[],[]]
	numberofMoves = 0
	whitePieceCount = 0
	blackPieceCount = 0
	def __init__(self):
		pass


	def createBoard(self, boardInput):
		'''Loop through text input and put into board by creating cell
		then the cell will create a piece if it is occupied by a @ or O or X'''
		for y in range(0, len(boardInput)):
			for x in range(0, len(boardInput[y])):
				self.board[y].append(self.createCell(x, y, boardInput[y][x]))
				if boardInput[y][x] == "@":
					self.blackPieceCount += 1
				elif boardInput[y][x] == "O":
					self.whitePieceCount += 1
		self.viewBoard()


	def viewBoard(self):
		#to view the board correctly
		for x in self.board:
			print(x)

	def validMovesCounter(self, oldX, oldY):
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
					blackMoves += self.validMovesCounter(x, y)
				else:
					whiteMoves += self.validMovesCounter(x, y)
		print(whiteMoves)
		print(blackMoves)


	def validMoves(self,oldX,newX,newY):
		if newX - oldX > 1:
			if (((newX < 8) and self.board[newY][newX].occupiedBy == " ") or
			 ((newX + 1 < 8)  and self.board[newY][newX + 1].occupiedBy == " ")):
				return True
		else:
			if (((newY < 8) and self.board[newY][oldX].occupiedBy == " ") or
			((oldY + 1 < 8) and self.board[oldY + 1][oldX].occupiedBy == " ")):
				return True

	def createCell(self, x, y, occupiedBy):
		"""Creates a cell. If the cell is occupied by a @ or ) or
			X it will create a piece that lies on top of the cell"""
		return c.Cell(x, y, occupiedBy)

	# def destorypiece():
	# 	destorypiec

	def jump(self, oldX, oldY, newX, newY):
		


	def move(self, oldX, oldY, newX, newY):
		'''Moves piece on board'''
	 #	check if player can move (NEED VALID MOVE)
	 if abs(newX - oldX) == 2 or abs(newY - oldY) == 2:
	 	if self.jump(oldX,oldY,newX,newY):
	 		self.board[oldY][oldX].changePiece(self.board[newY][newX])




	 if self.validMoves(oldX,oldY):
		self.board[oldY][oldX].changePiece(self.board[newY][newX])
	 else:
	 	print("FUCK OFF")

	def destorypiece(self, x, y):
		self.board[y][x].removePiece()