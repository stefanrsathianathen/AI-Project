class GameNode():
	"""docstring for node"""
	def __init__(self, move, value, board = None):
		self.move = move
		self.value = value
		self.board = board
		self.children = []

	def addChild(self, node):
		self.children.append(node)

	def defineParent(self, parent):
		self.parent = parent
