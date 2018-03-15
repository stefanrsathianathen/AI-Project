class Piece():
	"""docstring for Piece"""
	def __init__(self, x,y,kindOfPiece):
		self.x = x
		self.y = y
		self.kindOfPiece = kindOfPiece
	

	def __str__(self):
		return self.kindOfPiece

	def __repr__(self):
		return self.kindOfPiece

	def moveX(self,newX):
		#change the x
		self.x = newX


	def moveY(self,newY):
		self.y = newY