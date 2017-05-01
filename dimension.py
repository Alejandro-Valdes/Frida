import memory as m

class Dimension():
	def __init__(self, sup_lim, m, next):
		# By our language definition, the superior limit is always one shorter
		self.sup_lim = sup_lim - 1
		self.m = m
		self.next = next

class DimensionList():

	def __init__(self, sup_lim):
		self.r = 1
		self.dim = 1
		self.aux = 0

		dimension = Dimension(int(sup_lim), 0, None)

		self.first = dimension
		self.last = dimension

		self.r = (dimension.sup_lim + 1) * self.r

	def add_dimension(self, sup_lim):
		dimension = Dimension(int(sup_lim), 0, None)
		self.last.next = dimension
		self.last = dimension

		self.r = (dimension.sup_lim + 1) * self.r
		self.dim += 1

	def calculate_constants(self):
		tmp = self.first
		self.total_size = self.r

		while tmp:
			tmp.m = self.r / (self.first.sup_lim + 1)
			self.r = tmp.m
			tmp = tmp.next

	def __str__(self):
		aux = self.first
		stringRep = 'dims: ' + str(self.dim) + ' -> '

		if not aux:
			return None

		while aux:
			stringRep += 'lim: ' + str(aux.sup_lim) + ' m: ' + str(aux.m) + ' | '
			aux = aux.next

		stringRep += 'size: ' + str(self.total_size)

		return stringRep


