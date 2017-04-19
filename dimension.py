class Dimension():
	def __init__(self, lim_sup, m, next):
		# By our language definition, the superior limit is always one shorter
		self.lim_sup = lim_sup - 1
		self.m = m
		self.next = next

class DimensionList():

	def __init__(self, lim_sup):
		self.r = 1
		self.dim = 1
		self.aux = 0

		dimension = Dimension(int(lim_sup), 0, None)

		self.first = dimension
		self.last = dimension

		self.r = (dimension.lim_sup + 1) * self.r

	def add_dimension(self, lim_sup):
		dimension = Dimension(int(lim_sup), 0, None)
		self.last.next = dimension
		self.last = dimension

		self.r = (dimension.lim_sup + 1) * self.r
		self.dim += 1

	def calculate_constants(self):
		tmp = self.first
		self.total_size = self.r

		while tmp:
			tmp.m = self.r / (self.first.lim_sup + 1)
			self.r = tmp.m
			tmp = tmp.next

	def __str__(self):
		aux = self.first
		stringRep = 'dims: ' + str(self.dim) + ' -> '

		if not aux:
			return None

		while aux:
			stringRep += 'lim: ' + str(aux.lim_sup) + ' m: ' + str(aux.m) + ' | '
			aux = aux.next

		stringRep += 'size: ' + str(self.total_size)

		return stringRep


