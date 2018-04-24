class GameNode():
	"""docstring for node"""
	def __init__(self, Board,value,parent=None):
		self.board = Board
		self.weight = value
		self.parent = parent
		self.children = []
		
	def addChild(self,childNode):
		self.children.append(childNode)


class GameTree():

	def __init__(self):
		self.root = None

	def build_tree(self)