SymbolTable = {}

class Symbol(object):
	def __init__(self, type, id):
		self.type = type
		self.id = id

	def __str__(self):
		return '(type:{0}, id:{1})'.format(self.type, self.id)

class FunSymbol(Symbol):
	def __init__(self, type, id, params):
		super(FunSymbol, self).__init__(type, id)
		self.params = params

	def __str__(self):
		return '(type:{0}, id:{1}, params:{2})'.format(self.type, self.id, self.params)


class ArraySymbol(Symbol):
	def __init__(self, type, id, num):
		super(ArraySymbol, self).__init__(type, id)
		self.num = num

	def __str__(self):
		return '(type:{0}, id:{1}, num:{2})'.format(self.type, self.id, self.num)

