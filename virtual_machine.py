import sys
from memory import *

class VirtualMachine():
	def __init__(self, quad_list):
		self.quad_list = quad_list

	def run_list(self):
		print('\nOutput: ')
		i = 0
		for quad in self.quad_list:
			if quad.action == 200:
				print CteMemory.getItemValue(int(quad.res))