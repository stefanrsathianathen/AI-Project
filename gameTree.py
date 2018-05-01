class GameNode():
	"""docstring for node"""
	def __init__(self, board,move = None,value=0,parent=None):
		self.board = board
		self.value = value
		self.parent = parent
		self.children = []
		self.move = move
		# print(self.board)

	def addChild(self,childNode):
		self.children.append(childNode)

	def defineParent(self,psd):
		self.parent = psd
