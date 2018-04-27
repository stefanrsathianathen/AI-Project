class GameNode():
	"""docstring for node"""
	def __init__(self, board,move,value=0,parent=None):
		self.board = board
		self.weight = value
		self.parent = parent
		self.children = []
		self.move = move
		# print(self.board)

	def addChild(self,childNode):
		self.children.append(childNode)

	def defineParent(self,psd):
		self.parent = psd

# class GameTree():

# 	def __init__(self):
# 		self.root = None

# 	def build_tree(self)