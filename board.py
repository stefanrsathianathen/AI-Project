import Cell as c
import Player as p
class Board():
	"""docstring for Board"""

	board = [[],[],[],[],[],[],[],[]]
	numberofMoves = 0
	player1 = p.Player()

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

	def validMove(self, newX, newY):
		if (board[newX][newY].occupiedBy() == "-"):
			return True;
		return False;

	def findNumberOfMoves(self):

		totalMoves = 0;

		for row in range(0, len(board)):
			for x in range(0, len(row)):

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
