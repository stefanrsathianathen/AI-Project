#Marzuk Amin 824100
#Stefan Sathianathen 868514
class Cell():
	"""Piece"""

	def __init__(self, x, y, occupiedBy):
		self.x = x
		self.y = y
		if(occupiedBy != "-"):
			self.occupiedBy = occupiedBy
		else:
			self.occupiedBy = " "


	def __str__(self):
		return str(self.occupiedBy)


	def __repr__(self):
		return str(self.occupiedBy)

	def changePiece(self,otherCell):
		"""Swapping pieces when valid move"""
		temp = self.occupiedBy
		self.occupiedBy = otherCell.occupiedBy
		otherCell.occupiedBy = temp

	def removePiece(self):
		"""Deletes the piece from the board"""
		self.occupiedBy = " ";
