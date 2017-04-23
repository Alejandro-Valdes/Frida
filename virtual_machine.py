import sys
from memory import *
from semantic_cube import *
from symbol_table import *
import global_vars as g
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

def printUndefinedValue():
	print('Error: Acceso a variable indefinida')

class VirtualMachine():
	def __init__(self, quad_list):
		self.quad_list = quad_list
		self.mem = Memory()
		self.frida_gui = Tk()
		self.canvas = Canvas(self.frida_gui, width = 750, height = 600)
		self.canvas.pack()
		self.shapes = []

	def run_list(self):
		print('\nOutput: ')
		ip = 0
		fig_name = ''
		fig_param_stack = []
		paramAddresses = []
		currParam = 0
		ret_ip = 0
		memory_stack = []
		ip_exe_stack = []
		temp_local_mem = {}
		curr_scope = 'lienzo'
		
		while ip < len(self.quad_list):
			quad = self.quad_list[ip]

			if len(str(quad.o1)) > 0 and str(quad.o1)[0] == '*':
				quad.o1 = self.mem.getValue(int(quad.o1[1:]))
			if len(str(quad.o2)) > 0 and str(quad.o2)[0] == '*':
				quad.o2 = self.mem.getValue(int(quad.o2[1:]))
			if len(str(quad.res)) > 0 and str(quad.res)[0] == '*':
				quad.res = self.mem.getValue(int(quad.res[1:]))

			if quad.action == PRINT:
				if self.mem.getValue(int(quad.res)) is None:
					printUndefinedValue()
					sys.exit()

				if (self.mem.getValue(int(quad.res)) == TRUE):
					print('verdadero')
				elif (self.mem.getValue(int(quad.res)) == FALSE):
					print('falso')
				else:
					print(self.mem.getValue(int(quad.res)))

			elif quad.action == READ:
				if quad.res < 9000:
					print('error Lectura')
					sys.exit()

				elif quad.res >= 9000 and quad.res < 10000:
					bRes = input()
					if bRes == TRUE or bRes == FALSE:
						TempMemory.setValue(int(quad.res), bRes)
					else:
						print("Eso no es un bool")
						sys.exit()

				elif quad.res >= 10000 and quad.res < 11000:
					try:
						iRes = input()
						TempMemory.setValue(int(quad.res), int(iRes))
					except ValueError:
						print("Eso no es un entero")
						sys.exit()

				elif quad.res >= 11000 and quad.res < 12000:
					try:
						fRes = input()
						TempMemory.setValue(int(quad.res), float(fRes))
					except ValueError:
						print("Eso no es un decimal")
						sys.exit()

				elif quad.res >= 12000 and quad.res < 13000:
					sRes = input()
					TempMemory.setValue(int(quad.res), sRes)

				else:
					print('error lectura')
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
				if self.mem.getValue(int(quad.o1)) == FALSE:
					ip = int(quad.res) - 1
				else:
					pass

			elif quad.action == VERIFY:
				quad_o1 = self.mem.getValue(int(quad.o1))

				if int(quad_o1) >= int(quad.o2) and int(quad_o1) <= int(quad.res):
					pass
				else:
					print('Error: Indice fuera de limites de arreglo')

			elif quad.action > ANDORSTART and quad.action < ANDOREND:
				res = self.logic_operation(quad.action, quad.o1, quad.o2)
				self.mem.setValue(res, int(quad.res))

			elif quad.action == ERA:
				paramAddresses = SymbolsTable.get_function_params_addresses(quad.o1)	

				scoped_addresses = SymbolsTable.getScopedMemory(curr_scope)

				for address in scoped_addresses:
					temp_local_mem[int(address)] = self.mem.getValue(int(address))

				memory_stack.append(dict(temp_local_mem))

			elif quad.action == GOSUB:
				ip_exe_stack.append(ip)
				ip = int(quad.res) - 1
				currParam = 0

				curr_scope = str(quad.o1)

			elif quad.action == ENDPROC:
				ip = ip_exe_stack.pop()
				scoped_addresses = SymbolsTable.getScopedMemory(curr_scope)

				for address in scoped_addresses:
					self.mem.setValue(None, int(address))

				temp = {}
				temp = memory_stack.pop()

				for address in temp:
					self.mem.setValue(temp[address], int(address))

			elif quad.action == PARAM:
				if int(quad.o1.val) in temp_local_mem:
					value = temp_local_mem[int(quad.o1.val)]
					print (value)
				else:
					value = self.mem.getValue(int(quad.o1.val))

				self.mem.setValue(value, int(paramAddresses[currParam]))
				currParam += 1

			elif quad.action == FIG:
				fig_code = quad.o1

			elif quad.action == F_PAR:
				fig_param_stack.append(int(quad.res))

			elif quad.action == F_FIN:
				self.drawShape(fig_code, fig_param_stack, quad.res)

			#shape move TODO
			elif quad.action == 90000:
				self.mem 

			ip += 1

	def drawShape(self, fig_code, fig_param_stack, res_address):
		if fig_code.val == CUADRADO:
			color = self.mem.getValue(fig_param_stack.pop())
			pos_y = self.mem.getValue(fig_param_stack.pop())
			pos_x = self.mem.getValue(fig_param_stack.pop())
			sqr_len = self.mem.getValue(fig_param_stack.pop())
			cuad = self.canvas.create_rectangle(pos_x, pos_y, pos_x + sqr_len, pos_y + sqr_len, fill = color)
			self.mem.setValue(res_address, cuad)
			

	def relational_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if o1 is None or o2 is None:
			printUndefinedValue()
			sys.exit()

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
		print('Error relacional')
		sys.exit()

	def basic_math(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))		

		if o1 is None or o2 is None:
			print('Error: acceso a valor indefinido')
			sys.exit()

		if action == SUM:
			return o1 + o2
		elif action == SUB:
			return o1 - o2
		elif action == MULT:
			return o1 * o2
		elif action == DIV:
			return o1 / o2
		print('Error matematicas')

		sys.exit()

	def logic_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if o1 is None or o2 is None:
			print('Error: acceso a valor indefinido')
			sys.exit()

		o1 = True if o1 == TRUE else False
		o2 = True if o2 == TRUE else False

		if action == AND:
			return TRUE if o1 and o2 else FALSE
		elif action == OR:
			return TRUE if o1 or o2 else FALSE

		print('Error logica')
		sys.exit()

