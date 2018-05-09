class GameNode():
	"""docstring for node"""
	def __init__(self, move, value, board = None):
		self.move = move
		self.value = value
		self.board = board
		self.children = []
