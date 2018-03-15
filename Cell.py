import Piece as p
class Cell():
	"""docstring for Piece"""
	
	def __init__(self,x,y,occupiedBy):
		self.x = x
		self.y = y
		#check if the piece is ocuppied, if so create that piece
		#otherwise keep it as a blank cell
		if(occupiedBy != "-"):
			self.occupiedBy = self.createPiece(x,y, occupiedBy)
		else:
			self.occupiedBy = "-1"


	def __str__(self):
		return str(self.occupiedBy)


	def __repr__(self):
		return str(self.occupiedBy)


	def createPiece(self,x,y,occupiedBy):
		'''Creates piece that lies on top of the cell'''
		return p.Piece(x,y,occupiedBy)


	def destory(self):
		"""Getting rid of piece"""
		pass