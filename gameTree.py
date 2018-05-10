class gameNode():
	"""docstring for node"""
	def __init__(self, move = None,parent=None,value=None):
		self.value = value
		self.parent = parent
		self.children = []
		self.move = [move]
		# print(self.board)

	def addChild(self,childNode):
		self.children.append(childNode)

	def defineParent(self,psd):
		self.parent = psd

	def addParentMoves(self, previousMoves):

		for x in previousMoves[::-1]:
			self.move.insert(0,x)

#store all parent moves then my move in list. Then you dont need to store the whole board
