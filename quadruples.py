import sys

class QuadrupleItem():
	def __init__(self, action, o1, o2, res):
		self.action = action
		self.o1 = o1
		self.o2 = o2
		self.res = res

class  Quadruple():

	quadruple_list = []
	__shared_state = {}

	def __init__(self):
		self.__dict__ = sefl.__shared_state

	@classmethod
	def add_quad(cls, quadruple):
		cls.quadruple_list.append(quadruple)

	@classmethod
	def print_list(cls):
		print('\nQUADRUPLES: ')
		for quad in cls.quadruple_list:
			print quad.action + '\t' + quad.o1 + '\t' + quad.o2 + '\t' + quad.res