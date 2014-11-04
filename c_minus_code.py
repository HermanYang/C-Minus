ThreeAddressCodes = []

class Code:
	def __init__(self, op = None, src1 = None, src2 = None, des = None):
		self.op = op
		self.src1 = src1
		self.src2 = src2
		self.des = des

	def __str__(self):
		return 'op:{0}, src1:{1} src2:{2} des{3}'.format(self.op, self.src1, self.src2, self.des)

