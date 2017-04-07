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
					bRes = raw_input()
					if bRes == 'verdadero' or bRes == 'falso':
						TempMemory.setValue(int(quad.res), bRes)
					else:
						print 'Error: esperaba un bool'
						sys.exit()

				elif quad.res >= 10000 and quad.res < 11000:
					iRes = raw_input()
					TempMemory.setValue(int(quad.res), int(iRes))

				elif quad.res >= 11000 and quad.res < 12000:
					fRes = raw_input()
					TempMemory.setValue(int(quad.res), float(fRes))

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

