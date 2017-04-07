import sys
from memory import *
from semantic_cube import *
import global_vars as g

class VirtualMachine():
	def __init__(self, quad_list):
		self.quad_list = quad_list
		self.mem = Memory()

	def basic_math(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))
		if action == SUM:
			return o1 + o2
		elif action == SUB:
			return o1 - o2
		elif action == MULT:
			return o1 * o2
		elif action == DIV:
			return o1 / o2
		print 'Error'
		sys.exit()

	def relational_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if action == LTHAN:
			return 'verdadero' if o1 < o2 else 'falso' 
		elif action == GTHAN:
			return 'verdadero' if o1 > o2 else 'falso'
		elif action == EQUAL:
			return 'verdadero' if o1 == o2 else 'falso'
		elif action == DIFF:
			return 'verdadero' if o1 != o2 else 'falso'
		elif action == LETHAN:
			return 'verdadero' if o1 <= o2 else 'falso'
		elif action == GETHAN:
			return 'verdadero' if o1 >= o2 else 'falso'
		print 'Error'
		sys.exit()

	def basic_math(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if action == SUM:
			return o1 + o2
		elif action == SUB:
			return o1 - o2
		elif action == MULT:
			return o1 * o2
		elif action == DIV:
			return o1 / o2
		print 'Error'
		sys.exit()

	def run_list(self):
		print('\nOutput: ')
		i = 0
		
		for quad in self.quad_list:
			#print
			if quad.action == PRINT:
				print self.mem.getValue(int(quad.res))
			#read
			elif quad.action == READ:
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
			elif quad.action == ASSIGN:
				res = self.mem.getValue(int(quad.o1))
				self.mem.setValue(res, int(quad.res))

			elif quad.action > RELSTART and quad.action < RELEND:
				res = self.relational_operation(quad.action, quad.o1, quad.o2)
				self.mem.setValue(res, int(quad.res))

			elif quad.action > MATHSTART and quad.action < MATHEND:
				res = self.basic_math(quad.action, quad.o1, quad.o2)
				self.mem.setValue(res, int(quad.res))



