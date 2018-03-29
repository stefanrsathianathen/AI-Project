import math
class Node():
	"""docstring for Node"""
	def __init__(self, x, y, weight):
		self.x = x
		self.y = y
		self.l = None
		self.r = None
		self.weight = weight
		
class Tree():
	"""docstring for Tree"""
	def __init__(self):
		self.root = None

	#From Stack overflow https://stackoverflow.com/questions/2598437/how-to-implement-a-binary-tree
	def getRoot(self):
		return self.root

	def add(self, x,y):
		if(self.root == None):
			self.root = Node(x,y,0)
		else:
			self._add(x,y,self.calculateWeight(x,y), self.root)

	def _add(self, x, y, val, node):
		if(val < node.weight):
			if(node.l != None):
				self._add(x,y,val, node.l)
			else:
				node.l = Node(x,y,val)
		else:
			if(node.r != None):
				self._add(x,y,val, node.r)
			else:
				node.r = Node(x,y,val)

	def find(self, val):
		if(self.root != None):
			return self._find(val, self.root)
		else:
			return None

	def _find(self, val, node):
		if(val == node.weight):
			return node
		elif(val < node.weight and node.l != None):
			self._find(val, node.l)
		elif(val > node.weight and node.r != None):
			self._find(val, node.r)

	def printTree(self):
		if(self.root != None):
			self._printTree(self.root)

	def _printTree(self, node):
		if(node != None):
			self._printTree(node.l)
			print( str(node.weight )+ "    ")
			self._printTree(node.r)


	def calculateWeight(self, newX, newY):
		return math.sqrt(((newX-self.root.x)**2) + ((newY-self.root.y)**2))