import sys
from virtual_machine import VirtualMachine
from semantic_cube import *

class QuadrupleItem():
	def __init__(self, action, o1, o2, res):
		self.action = action
		self.o1 = o1
		self.o2 = o2
		self.res = res

class Quadruple():

	quadruple_list = []
	__shared_state = {}

	def __init__(self):
		self.__dict__ = self.__shared_state

	@classmethod
	def add_quad(cls, quadruple):
		cls.quadruple_list.append(quadruple)

	@classmethod
	def print_list(cls):
		i = 0
		for quad in cls.quadruple_list:
			print(str(i) + '\t' + getOperationStr(quad.action) + '\t' + str(quad.o1) + '\t' + str(quad.o2) + '\t' + str(quad.res))
			i +=1

	# @classmethod
	# def run_list(cls):
	# 	vm = VirtualMachine(cls.quadruple_list)
	# 	vm.run_list()