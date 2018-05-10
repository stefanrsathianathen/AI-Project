#Marzuk Amin 824100
#Stefan Sathianathen 868514
import math
class Node():
	"""Node"""
	def __init__(self, x, y, weight, piece):
		self.x = x
		self.y = y
		self.piece = piece
		self.weight = weight

class Tree():
	"""Tree"""
	def __init__(self):
		self.nodes = []


	def add(self, x,y, piece):
		'''add node to the tree'''
		if(len(self.nodes) == 0):
			self.nodes.append( Node(x,y,0,piece))
		else:
			self.nodes.append(Node(x,y,self.calculateWeight(x,y), piece))


	def calculateWeight(self, newX, newY):
		'''Find the distance between the first piece
			entered into tree and new node'''
		return math.sqrt(((newX-self.nodes[0].x)**2) +
							((newY-self.nodes[0].y)**2))
