import sys
from memory import *
from semantic_cube import *
import global_vars as g

GOTO = 'GoTo'
GOTOF = 'GoToF'
TRUE = 'verdadero'
FALSE = 'falso'

class VirtualMachine():
	def __init__(self, quad_list):
		self.quad_list = quad_list
		self.mem = Memory()

	def run_list(self):
		print('\nOutput: ')
		ip = 0
		
		while ip < len(self.quad_list):
			quad = self.quad_list[ip]

			if quad.action == PRINT:
				print self.mem.getValue(int(quad.res))

			elif quad.action == READ:
				if quad.res < 9000:
					print 'error'
					sys.exit()

				elif quad.res >= 9000 and quad.res < 10000:
					bRes = raw_input()
					if bRes == 'verdadero' or bRes == 'falso':
						TempMemory.setValue(int(quad.res), bRes)
					else:
						print("Eso no es un bool")
						sys.exit()

				elif quad.res >= 10000 and quad.res < 11000:
					try:
						iRes = raw_input()
						TempMemory.setValue(int(quad.res), int(iRes))
					except ValueError:
						print("Eso no es un entero")
						sys.exit()

				elif quad.res >= 11000 and quad.res < 12000:
					try:
						fRes = raw_input()
						TempMemory.setValue(int(quad.res), float(fRes))
					except ValueError:
						print("Eso no es un decimal")
						sys.exit()

				elif quad.res >= 12000 and quad.res < 13000:
					sRes = raw_input()
					TempMemory.setValue(int(quad.res), sRes)

				else:
					print 'error'
					sys.exit()

			elif quad.action == ASSIGN:
				res = self.mem.getValue(int(quad.o1))
				self.mem.setValue(res, int(quad.res))

			elif quad.action > RELSTART and quad.action < RELEND:
				res = self.relational_operation(quad.action, quad.o1, quad.o2)
				self.mem.setValue(res, int(quad.res))

			elif quad.action > MATHSTART and quad.action < MATHEND:
				res = self.basic_math(quad.action, quad.o1, quad.o2)
				self.mem.setValue(res, int(quad.res))

			elif quad.action == GOTO:
				ip = int(quad.res) - 1

			elif quad.action == GOTOF:
				if self.mem.getValue(int(quad.o1)) == 'falso':
					ip = int(quad.res) - 1
				else:
					pass

			elif quad.action > ANDORSTART and quad.action < ANDOREND:
				res = self.and_or_operation(quad.action, quad.o1, quad.o2)
				self.mem.setValue(res, int(quad.res))

			ip += 1

	def relational_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if action == LTHAN:
			return TRUE if o1 < o2 else FALSE 
		elif action == GTHAN:
			return TRUE if o1 > o2 else FALSE
		elif action == EQUAL:
			return TRUE if o1 == o2 else FALSE
		elif action == DIFF:
			return TRUE if o1 != o2 else FALSE
		elif action == LETHAN:
			return TRUE if o1 <= o2 else FALSE
		elif action == GETHAN:
			return TRUE if o1 >= o2 else FALSE
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

	def and_or_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		o1 = True if o1 == TRUE else False
		o2 = True if o2 == TRUE else False

		if action == AND:
			return TRUE if o1 and o2 else FALSE
		elif action == OR:
			return TRUE if o1 or o2 else FALSE

		print 'Error'
		sys.exit()



