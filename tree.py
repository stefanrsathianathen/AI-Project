import math
class Node():
	"""docstring for Node"""
	def __init__(self, x, y, weight, piece):
		self.x = x
		self.y = y
		self.piece = piece
		self.weight = weight

class Tree():
	"""docstring for Tree"""
	def __init__(self):
		self.nodes = []

	#From Stack overflow https://stackoverflow.com/questions/2598437/how-to-implement-a-binary-tree


	def add(self, x,y, piece):
		if(len(self.nodes) == 0):
			self.nodes.append( Node(x,y,0,piece))
		else:
			self.nodes.append(Node(x,y,self.calculateWeight(x,y), piece))

	def printD(self):
		self.nodes.sort(key=lambda x: x.weight, reverse=False)
		for x in self.nodes:
			print(x.piece)


	def calculateWeight(self, newX, newY):
		return math.sqrt(((newX-self.nodes[0].x)**2) + ((newY-self.nodes[0].y)**2))
