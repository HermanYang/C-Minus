class Node:
	def __init__(self, type, value = None):
		self.parent = None
		self.type = type
		self.value = value
		self.children = []

	def setType(self, type):
		assert type 
		self.type = type

	def setValue(self, value):
		assert value 
		self.value = value

	def addChild(self, node):
		assert node 
		assert node != self
		node.parent = self
		self.children.append(node)

	def removeChild(self, node):
		self.children.remove(node)

	def getFirstChildByType(self, type):
		s = []

		for c in reversed(self.children):
			s.append(c)

		while len(s) > 0:
			n = s.pop()
			if n.type == type:
				return n
			else:
				for c in reversed(n.children):
					s.append(c)
		return None

	def getChildrenByType(self, type):	

		s = []
		children = []

		for c in reversed(self.children):
			s.append(c)

		while len(s) > 0:
			n = s.pop()
			if n.type == type:
				children.append(n)
			else:
				for c in reversed(n.children):
					s.append(c)

		return children

	def getChildrenByValue(self, value):	

		s = []
		children = []

		for c in reversed(self.children):
			s.append(c)

		while len(s) > 0:
			n = s.pop()
			if n.value == value:
				children.append(n)
			else:
				for c in reversed(n.children):
					s.append(c)

		return children

	def getFirstChildByValue(self, value):
		s = []

		for c in reversed(self.children):
			s.append(c)

		while len(s) > 0:
			n = s.pop()
			if n.value == value:
				return n
			else:
				for c in reversed(n.children):
					s.append(c)
		return None


	def __str__(self):
		if self.value:
			return 'node type:{0} value:{1}'.format(self.type, self.value)
		else:
			return 'node type:{0}'.format(self.type)
