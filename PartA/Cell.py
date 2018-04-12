#Marzuk Amin 
#Stefan Sathianathen 868514
class Cell():
	"""Piece"""

	def __init__(self, x, y, occupiedBy):
		self.x = x
		self.y = y
		#check if the piece is ocuppied, if so create that piece
		#otherwise keep it as a blank cell
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
