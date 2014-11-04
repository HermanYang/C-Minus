class Token:
	def __init__(self, type, value, lineNum):
		self.type = type
		self.value = value
		self.lineNum = lineNum

	def __str__(self):
		type = self.type
		if type == 'identifier':
			type = 'id'
		return '(type {0}    value {1}    lineNum {2})'.format(type, self.value, self.lineNum)