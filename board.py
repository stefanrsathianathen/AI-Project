import Cell as c
import tree as t
import math
class Board():
	"""docstring for Board"""

	board = [[],[],[],[],[],[],[],[]]
	numberofMoves = 0
	whitePieceCount = 0
	blackPieceCount = 0
	tree = t.Tree()

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

		if ((self.isValidMove(oldX, oldY, oldX + 1, oldY)) or
			 (self.isValidMove(oldX, oldY, oldX + 2, oldY))):
			netMoves += 1
		if ((self.isValidMove(oldX, oldY, oldX - 1, oldY)) or
			 (self.isValidMove(oldX, oldY, oldX - 2, oldY))):
			netMoves += 1
		if ((self.isValidMove(oldX, oldY, oldX, oldY + 1)) or
			(self.isValidMove(oldX, oldY, oldX, oldY + 2))):
			netMoves += 1
		if ((self.isValidMove(oldX, oldY, oldX, oldY - 1)) or
			 (self.isValidMove(oldX, oldY, oldX, oldY - 2))):
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

	def createCell(self, x, y, occupiedBy):
		"""Creates a cell. If the cell is occupied by a @ or ) or
			X it will create a piece that lies on top of the cell"""
		return c.Cell(x, y, occupiedBy)

	def move(self, oldX, oldY, newX, newY):
		'''Moves piece on board'''
	#	check if player can move (NEED VALID MOVE)
		if self.isValidMove(oldX, oldY, newX, newY):
			self.board[oldY][oldX].changePiece(self.board[newY][newX])

		pieceType = self.board[newY][newX].__str__()

		if pieceType == "O":
			opponentPiece = "@"
		else:
			opponentPiece = "O"

		self.eliminatePieces(newX,newY,pieceType,opponentPiece)


	def isValidMove(self, oldX, oldY, newX, newY):

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
		if (self.board[y][x].occupiedBy == "@"):
			self.blackPieceCount -= 1
		elif (self.board[y][x].occupiedBy == "O"):
			self.whitePieceCount -= 1
		self.board[y][x].removePiece()

	def eliminatePieces(self, x, y, pieceType, opponentPiece):

	    if (self.board[y][x + 1].occupiedBy == opponentPiece and
	        self.board[y][x + 2].occupiedBy == pieceType):
	        self.destoryPiece(x + 1, y)
	    elif (self.board[y][x - 1].occupiedBy == opponentPiece and
	        self.board[y][x - 2].occupiedBy == pieceType):
	        self.destoryPiece(x - 1, y)
	    elif (self.board[y + 1][x].occupiedBy == opponentPiece and
	        self.board[y + 2][x].occupiedBy == pieceType):
	        self.destoryPiece(x, y + 1)
	    elif (self.board[y - 1][x].occupiedBy == opponentPiece and
	        self.board[y - 2][x].occupiedBy == pieceType):
	        self.destoryPiece(x, y - 1)
	    elif (self.board[y][x + 1].occupiedBy == opponentPiece and
	        self.board[y][x - 1].occupiedBy == opponentPiece):
	        self.destoryPiece(x, y)
	    elif (self.board[y + 1][x].occupiedBy == opponentPiece and
	        self.board[y - 1][x].occupiedBy == opponentPiece):
	        self.destoryPiece(x, y)

	def createTree(self):
		for y in range(0, len(self.board)):
			for x in range(0, len(self.board[y])):
				if (self.board[y][x].occupiedBy != 'X' and
					self.board[y][x].occupiedBy != ' '):
					self.tree.add(x,y,self.board[y][x].occupiedBy)
		self.tree.printD()

	def searchTree(self):

		for x in range(0, len(self.tree.nodes)):
			if (self.tree.nodes[x].piece == "@"):
				closestPieces = self.findClosestPieces(x)

				for j in range(0,2):
					xdiff = self.tree.nodes[x].x-closestPieces[j].x
					ydiff = self.tree.nodes[x].y-closestPieces[j].y

					if (xdiff < ydiff):
						while (xdiff != 0):
							self.move(closestPieces[j].x, closestPieces[j].y,
							closestPieces[j].x-1, closestPieces[j].y)
							self.viewBoard()
							xdiff = self.tree.nodes[x].x-closestPieces[j].x
							print(xdiff)
						while (abs(ydiff) != 1):
							self.move(closestPieces[j].x, closestPieces[j].y,
							closestPieces[j].x, closestPieces[j].y-1)
							self.viewBoard()
							ydiff = self.tree.nodes[x].y-closestPieces[j].y
					else:
						while (ydiff != 0):
							self.move(closestPieces[j].x, closestPieces[j].y,
							closestPieces[j].x, closestPieces[j].y-1)
							self.viewBoard()
							ydiff = self.tree.nodes[x].y-closestPieces[j].y
						while (abs(xdiff) != 1):
							self.move(closestPieces[j].x, closestPieces[j].y,
							closestPieces[j].x-1, closestPieces[j].y)
							self.viewBoard()
							xdiff = self.tree.nodes[x].x-closestPieces[j].x
							print(xdiff)




	def findClosestPieces(self, index):
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

	def distanceFormula(self,x1,y1,x2,y2):
		return math.sqrt(((x1-x2)**2) + ((y1-y2)**2))
