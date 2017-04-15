class Dimension():
	def __init__(self, lim_sup, next):
		# By our language definition, the superior limit is always one shorter
		self.lim_sup = lim_sup - 1
		self.next = next

class DimensionList():

	def __init__(self, lim_sup):
		self.r = 1
		self.dim = 1

		dimension = Dimension(int(lim_sup), None)

		self.first = dimension
		self.last = dimension

		self.r = (dimension.lim_sup + 1) * self.r

	def add_dimension(self, lim_sup):
		dimension = Dimension(int(lim_sup), None)
		self.last.next = dimension
		self.last = dimension

		self.r = (dimension.lim_sup + 1) * self.r
		self.dim += 1

	# def calculate_constant(self):
	# 	tmp = first
	# 	self.totalSize = self.r

	# 	while first.next:
	# 		m = self.r / (self.first.lim_sup + 1)
	# 		self.r = m

	def __str__(self):
		aux = self.first
		stringRep = 'dims: ' + str(self.dim) + ' -> '

		if not aux:
			return None

		while aux:
			stringRep += str(aux.lim_sup) + ' '
			aux = aux.next

		stringRep += 'size: ' + str(self.r)

		return stringRep


