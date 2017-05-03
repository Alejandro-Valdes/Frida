import sys
from virtual_machine import VirtualMachine
from semantic_cube import *

class QuadrupleItem():
	"""Clase QuadrupleItem

	Esta clase representa un cuádruplo 
	"""

	def __init__(self, action, o1, o2, res):
		"""Inicializador default"""

		self.action = action
		self.o1 = o1
		self.o2 = o2
		self.res = res

class Quadruple():
	"""Clase Quadruple

	Representa un objeto estático que maneja las 
	funciones relacionadas a cuádruplos y la misma
	lista de cuádruplos
	"""

	quadruple_list = [] # Lista de cuádruplos
	__shared_state = {}

	def __init__(self):
		"""Inicializador por default"""
		self.__dict__ = self.__shared_state

	@classmethod
	def add_quad(cls, quadruple):
		"""Añade el cuádruplo a la lista de cuádruplos
		
		args: 
			quadruple -- cuádruplo a añadir 
		"""
		cls.quadruple_list.append(quadruple)

	@classmethod
	def print_list(cls):
		"""Función auxiliar que muestra la lista de cuádruplos en consola
		"""

		i = 0
		for quad in cls.quadruple_list:
			print(str(i) + '\t' + getOperationStr(quad.action) + '\t' + str(quad.o1) + '\t' + str(quad.o2) + '\t' + str(quad.res))
			i +=1

	# Previous way of running file compilation and execution
	# @classmethod
	# def run_list(cls):
	# 	vm = VirtualMachine(cls.quadruple_list)
	# 	vm.run_list()