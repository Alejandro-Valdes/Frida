import memory as m

class Dimension():
	"""Clase Dimension
	
	Pensada como el nodo de una lista ligada. No maneja k por motivos de conveniencia, pero la implementación
	de arreglos multidimensionales requiere de cambios no tan complicados.
	"""

	def __init__(self, sup_lim, m, next):
		"""Por definición, nuestro lenguaje siempre tiene como limite inferior de un arreglo el número 0

		args:
			sup_lim -- limite superior de la dimensión
			m -- constante m que se utiliza como multiplicador
			next -- apuntador a nulo o a siguiente nodo
		"""
		self.sup_lim = sup_lim - 1
		self.m = m
		self.next = next

class DimensionList():
	"""Clase DimensionList
	
	Lista encadenada que utiliza objetos tipo Dimension como nodos
	"""

	def __init__(self, sup_lim):
		"""Inicializador de clase DimensionList
		
		args:
			sup_lim -- tamaño de dimensión con la que sera inicializada la lista
		"""
		self.r = 1
		self.dim = 1
		self.aux = 0

		dimension = Dimension(int(sup_lim), 0, None) # creación de primera dimension de la lista

		self.first = dimension
		self.last = dimension

		self.r = (dimension.sup_lim + 1) * self.r # cálculo de r, para al final obtener el tamaño de arreglo

	def add_dimension(self, sup_lim):
		"""Método utilidad que permite añadir dimensiones a la lista que mantiene esta clase

		args:
			sup_lim -- tamaño superior de nueva dimensión
		"""
		dimension = Dimension(int(sup_lim), 0, None)
		self.last.next = dimension
		self.last = dimension

		self.r = (dimension.sup_lim + 1) * self.r # cálculo de r
		self.dim += 1

	def calculate_constants(self):
		"""Método que calcula las constantes del arreglo cuando éste se ha terminado de definir"""
		tmp = self.first
		self.total_size = self.r # guardamos el tamaño total del arreglo

		while tmp:
			tmp.m = self.r / (self.first.sup_lim + 1)
			self.r = tmp.m
			tmp = tmp.next

	def __str__(self):
		"""Método que imprime el arreglo de forma personalizada""" 
		aux = self.first
		stringRep = 'dims: ' + str(self.dim) + ' -> '

		if not aux:
			return None

		while aux: # por cada dimensión de este arreglo
			stringRep += 'lim: ' + str(aux.sup_lim) + ' m: ' + str(aux.m) + ' | ' # mostrar detalles de dimensións
			aux = aux.next

		stringRep += 'size: ' + str(self.total_size)

		return stringRep


