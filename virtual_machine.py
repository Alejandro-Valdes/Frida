import sys
from memory import *
from semantic_cube import *
from symbol_table import *
import global_vars as g
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import turtle

def printUndefinedValue():
	print('Error: Acceso a variable indefinida')

class VirtualMachine():
	def __init__(self, quad_list):
		self.quad_list = quad_list
		self.mem = Memory()
		self.frida_gui = tk.Tk()
		self.frida_gui.title('Canvas')
		self.canvas = tk.Canvas(self.frida_gui, width = 750, height = 600)
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
		memory_to_save = []

		temp_local_mem = {}
		curr_scope = 'lienzo'

		start_lienzo_scope = int(self.quad_list[0].res)

		
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
					if bRes == 'verdadero':
						TempMemory.setValue(int(quad.res), TRUE)

					elif bRes == 'falso':
						TempMemory.setValue(int(quad.res), FALSE)

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
					TempMemory.setValue(int(quad.res), str(sRes))

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
				bool_res = self.mem.getValue(int(quad.o1))
				if bool_res is None:
					print('Error: variable indefinida')
					sys.exit()

				if bool_res == FALSE:
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

				#get memory that will be saved after the return or endproc	

				scoped_addresses = SymbolsTable.getScopedMemory(curr_scope)

				for address in scoped_addresses:
					temp_local_mem[int(address)] = self.mem.getValue(int(address))

				memory_stack.append(dict(temp_local_mem))
				memory_to_save.append(SymbolsTable.checkVarAddress(curr_scope, quad.o1))

			elif quad.action == GOSUB:
				ip_exe_stack.append(ip)
				ip = int(quad.res) - 1
				currParam = 0
				curr_scope = str(quad.o1)


			elif quad.action == ENDPROC:
				#EXTRACT TO OWN FUNC ITS THE SAME AS RET
				ip = ip_exe_stack.pop()
				if(ip > start_lienzo_scope):
					curr_scope = 'lienzo'
				scoped_addresses = SymbolsTable.getScopedMemory(curr_scope)

				for address in scoped_addresses:
					self.mem.setValue(None, int(address))

				temp = {}
				temp = memory_stack.pop()

				for address in temp:
					self.mem.setValue(temp[address], int(address))

				#END EXTRACT	
			
				memory_to_save.pop()

			elif quad.action == PARAM:
				if int(quad.o1) in temp_local_mem:
					value = temp_local_mem[int(quad.o1)]
					if value is None:
						print (temp_local_mem)
						print(self.mem.getValue(int(quad.o1)))

				else:
					value = self.mem.getValue(int(quad.o1))

				self.mem.setValue(value, int(paramAddresses[currParam]))
				currParam += 1

			elif quad.action == RET:
				resMem = quad.res
				resValue = self.mem.getValue(int(resMem))

				#EXTRACT TO OWN FUNC ITS THE SAME AS ENDPROC
				ip = ip_exe_stack.pop()
				if(ip > start_lienzo_scope):
					curr_scope = 'lienzo'
				scoped_addresses = SymbolsTable.getScopedMemory(curr_scope)

				for address in scoped_addresses:
					self.mem.setValue(None, int(address))

				temp = {}
				temp = memory_stack.pop()

				for address in temp:
					self.mem.setValue(temp[address], int(address))

				#END EXTRACT				

				#save the value of the return
				res_address = memory_to_save.pop()
				self.mem.setValue(resValue, int(res_address))


			elif quad.action == FIG:
				fig_code = quad.o1

			elif quad.action == F_PAR:
				fig_param_stack.append(int(quad.res))

			elif quad.action == F_FIN:

				if fig_code == PINCEL:
					self.drawBrush(fig_param_stack, quad.res)

				else:
					self.drawShape(fig_code, fig_param_stack, quad.res)

			#shape move TODO
			elif quad.action == 90000:
				print('desplazar')

			ip += 1
			self.frida_gui.update()

		self.frida_gui.mainloop()

	def drawBrush(self, fig_param_stack, res_address):

		color = self.mem.getValue(fig_param_stack.pop())

		# create a turtle object
		ttl = turtle.RawTurtle(self.canvas)

		# draw equilateral triangle
		ttl.color(color)
		ttl.speed('fastest')
		ttl.shape('circle')


	def drawShape(self, fig_code, fig_param_stack, res_address):

		color = self.mem.getValue(fig_param_stack.pop())
		pos_y = self.mem.getValue(fig_param_stack.pop())
		pos_x = self.mem.getValue(fig_param_stack.pop())
		fig = 0

		if fig_code == CUADRADO:
			sqr_len = self.mem.getValue(fig_param_stack.pop())
			fig = self.canvas.create_rectangle(pos_x, pos_y, pos_x + sqr_len, pos_y + sqr_len, fill = color)

		elif fig_code == RECTANGULO:
			height = self.mem.getValue(fig_param_stack.pop())
			width = self.mem.getValue(fig_param_stack.pop())
			fig = self.canvas.create_rectangle(pos_x, pos_y, pos_x + width, pos_y + height, fill = color)

		elif fig_code == CIRCULO:
			cir_di = self.mem.getValue(fig_param_stack.pop()) * 2
			fig = self.canvas.create_oval(pos_x, pos_y, pos_x + cir_di, pos_y + cir_di, fill = color)

		elif fig_code == TRIANGULO:
			p3_y = pos_y
			p3_x = pos_x
			p2_y = self.mem.getValue(fig_param_stack.pop())
			p2_x = self.mem.getValue(fig_param_stack.pop())
			p1_y = self.mem.getValue(fig_param_stack.pop())
			p1_x = self.mem.getValue(fig_param_stack.pop())
			points = [p1_x, p1_y, p2_x, p2_y, p3_x, p3_y]
			fig = self.canvas.create_polygon(points, fill = color)


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

