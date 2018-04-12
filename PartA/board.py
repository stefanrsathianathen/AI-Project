#Marzuk Amin 824100
#Stefan Sathianathen 868514
import Cell as c
import tree as t
import math

class Board():
	"""Board class"""

	'''game board'''
	board = [[],[],[],[],[],[],[],[]]
	'''number of white pieces on board'''
	whitePieceCount = 0
	'''number of black pieces on board'''
	blackPieceCount = 0
	'''Tree for searching moves'''
	tree = t.Tree()

	def __init__(self):
		pass


	def createBoard(self, boardInput):
		'''Loop through text input and put into board by creating cell then the
		 	cell will create a piece if it is occupied by a @ or O or X'''
		for y in range(0, len(boardInput)):
			for x in range(0, len(boardInput[y])):
				self.board[y].append(self.createCell(x, y, boardInput[y][x]))
				if boardInput[y][x] == "@":
					self.blackPieceCount += 1
				elif boardInput[y][x] == "O":
					self.whitePieceCount += 1


	def validMovesCounter(self, oldX, oldY):
		'''Count how many valid moves a piece can make given the
			current board position and return that'''
		netMoves = 0;

		''' Move to the right '''
		if ((self.isValidMove(oldX, oldY, oldX + 1, oldY)) or
			 (self.isValidMove(oldX, oldY, oldX + 2, oldY))):
			netMoves += 1
		''' Move to the left '''
		if ((self.isValidMove(oldX, oldY, oldX - 1, oldY)) or
			 (self.isValidMove(oldX, oldY, oldX - 2, oldY))):
			netMoves += 1
		''' Move down '''
		if ((self.isValidMove(oldX, oldY, oldX, oldY + 1)) or
			(self.isValidMove(oldX, oldY, oldX, oldY + 2))):
			netMoves += 1
		''' Move up '''
		if ((self.isValidMove(oldX, oldY, oldX, oldY - 1)) or
			 (self.isValidMove(oldX, oldY, oldX, oldY - 2))):
			netMoves += 1
		return netMoves


	def findNumberOfMoves(self):
		'''Calculate the number of total moves the white and
		 	black pieces can make without moving anything'''
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


	def createCell(self, x, y, occupiedBy):
		"""Creates a cell. If the cell is occupied by a @ or ) or
			X it will create a piece that lies on top of the cell"""
		return c.Cell(x, y, occupiedBy)


	def move(self, oldX, oldY, newX, newY):
		'''Moves piece on board and check if need to elimate pieces,
			if so elimate them'''
		if self.isValidMove(oldX, oldY, newX, newY):
			self.board[oldY][oldX].changePiece(self.board[newY][newX])

		pieceType = self.board[newY][newX].__str__()

		if pieceType == "O":
			opponentPiece = "@"
		else:
			opponentPiece = "O"

		self.eliminatePieces(newX, newY, pieceType, opponentPiece)


	def isValidMove(self, oldX, oldY, newX, newY):
		'''Check if move is valid and return if okay'''
		if (oldX > 7 or oldX < 0 or newX > 7 or newX < 0 or
			oldY > 7 or oldY < 0 or newY > 7 or newY < 0):
			return False
		elif (abs(newX - oldX) > 2 or abs (newY - oldY) > 2):
			return False

		if self.board[newY][newX].occupiedBy == " ":
			return True
		else:
			return False


	def destoryPiece(self, x, y):
		'''Destory the piece if it is no longer needed'''
		if (self.board[y][x].occupiedBy == "@"):
			self.blackPieceCount -= 1
		elif (self.board[y][x].occupiedBy == "O"):
			self.whitePieceCount -= 1
		self.board[y][x].removePiece()


	def eliminatePieces(self, x, y, pieceType, opponentPiece):
		'''Figure out if a piece needs to be elimated
			by game rules if so eliminate the piece'''
		if ((x + 2 < 8) and self.board[y][x + 1].occupiedBy == opponentPiece and
	        (self.board[y][x + 2].occupiedBy == pieceType or
			self.board[y][x + 2].occupiedBy == "X")):
			self.destoryPiece(x + 1, y)
		elif ((x - 2 >= 0) and self.board[y][x - 1].occupiedBy == opponentPiece
			and (self.board[y][x - 2].occupiedBy == pieceType or
			self.board[y][x -2].occupiedBy == "X")):
			self.destoryPiece(x - 1, y)
		elif ((y + 2 < 8) and self.board[y + 1][x].occupiedBy == opponentPiece
			and (self.board[y + 2][x].occupiedBy == pieceType or
			self.board[y + 2][x].occupiedBy == "X")):
			self.destoryPiece(x, y + 1)
		elif ((y - 2 >= 0) and self.board[y - 1][x].occupiedBy == opponentPiece
			and (self.board[y - 2][x].occupiedBy == pieceType or
			self.board[y - 2][x].occupiedBy == "X")):
			self.destoryPiece(x, y - 1)
		elif ((x + 1 < 8) and (x - 1 >= 0) and
			self.board[y][x + 1].occupiedBy == opponentPiece and
			self.board[y][x - 1].occupiedBy == opponentPiece):
			self.destoryPiece(x, y)
		elif ((y + 1 < 8) and (y - 1 >= 0) and
			self.board[y + 1][x].occupiedBy == opponentPiece and
			self.board[y - 1][x].occupiedBy == opponentPiece):
			self.destoryPiece(x, y)


	def createTree(self):
		'''Create tree with all valid pieces in board'''
		for y in range(0, len(self.board)):
			for x in range(0, len(self.board[y])):
				if (self.board[y][x].occupiedBy != 'X' and
					self.board[y][x].occupiedBy != ' '):
					self.tree.add(x,y,self.board[y][x].occupiedBy)


	def searchTree(self):
		'''Find and move pieces to elimate all the black pieces on board'''
		for x in range(0, len(self.tree.nodes)):
			if (self.tree.nodes[x].piece == "@"):
				closestPieces = self.findClosestPieces(x)

				for j in range(0,2):

					xdiff = self.tree.nodes[x].x - closestPieces[j].x
					ydiff = self.tree.nodes[x].y - closestPieces[j].y

					if (abs(xdiff) <= abs(ydiff)):

						while (xdiff != 0):
							if (xdiff < 0):
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x - 1) + ", " +
									str(closestPieces[j].y) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x - 1, closestPieces[j].y)
								xdiff += 1
								closestPieces[j].x -= 1
							else:
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x + 1) + ", " +
									str(closestPieces[j].y) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x + 1, closestPieces[j].y)
								xdiff -= 1
								closestPieces[j].x += 1

						while (abs(ydiff) != 1):
							if (ydiff < 1):
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x ) + ", " +
									str(closestPieces[j].y - 1) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x, closestPieces[j].y - 1)
								ydiff += 1
								closestPieces[j].y -= 1
							else:
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x ) + ", " +
									str(closestPieces[j].y + 1) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x, closestPieces[j].y + 1)
								ydiff -= 1
								closestPieces[j].y += 1

					else:
						while (ydiff != 0):
							if (ydiff < 0):
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x ) + ", " +
									str(closestPieces[j].y - 1) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x, closestPieces[j].y - 1)
								ydiff += 1
								closestPieces[j].y -= 1
							else:
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x ) + ", " +
									str(closestPieces[j].y + 1) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x, closestPieces[j].y + 1)
								ydiff -= 1
								closestPieces[j].y += 1

						while (abs(xdiff) != 1):
							if (xdiff < 1):
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x  - 1) + ", " +
									str(closestPieces[j].y) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x - 1, closestPieces[j].y)
								xdiff += 1
								closestPieces[j].x -= 1
							else:
								print("("+ str(closestPieces[j].x) + ", " +
									str(closestPieces[j].y) + ") -> (" +
									str(closestPieces[j].x  + 1) + ", " +
									str(closestPieces[j].y) + ")")

								self.move(closestPieces[j].x, closestPieces[j].y,
								closestPieces[j].x + 1, closestPieces[j].y)
								xdiff -= 1
								closestPieces[j].x += 1


	def findClosestPieces(self, index):
		'''Find and select the closest pieces to the current
			piece that we are trying to elimate'''
		closestPieces = []
		difference = 1

		while (len(closestPieces) != 2):
			if (index + difference < len(self.tree.nodes) and
				self.tree.nodes[index + difference].piece == "O"):
				closestPieces.append(self.tree.nodes[index + difference])
			if (index - difference >= 0 and
				self.tree.nodes[index - difference].piece == "O"):
				closestPieces.append(self.tree.nodes[index - difference])

			difference += 1
		return closestPieces
