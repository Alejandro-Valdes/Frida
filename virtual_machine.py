import sys
from memory import *
import global_vars as g

class VirtualMachine():
	def __init__(self, quad_list):
		self.quad_list = quad_list

	def run_list(self):
		print('\nOutput: ')
		i = 0
		mem = Memory()
		for quad in self.quad_list:
			#print
			if quad.action == 200:
				print mem.getValue(int(quad.res))
				
			#read
			elif quad.action == 300:
				if quad.res < 9000:
					print 'error'
					sys.exit()
				elif quad.res >= 9000 and quad.res < 10000:
					pass
				elif quad.res >= 10000 and quad.res < 11000:
					pass
				elif quad.res >= 11000 and quad.res < 12000:
					pass
				elif quad.res >= 12000 and quad.res < 13000:
					sRes = raw_input()
					TempMemory.setValue(int(quad.res), sRes)
				else:
					print 'error'
					sys.exit()

			#assign
			elif quad.action == 50:
				res = mem.getValue(int(quad.o1))
				mem.setValue(res, int(quad.res))

