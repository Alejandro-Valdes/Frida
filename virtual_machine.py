import sys
from memory import *
from semantic_cube import *
from symbol_table import *
import global_vars as g
from frida_gui import *
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import turtle

def printUndefinedValue():
	raise Exception('Error: Acceso a variable indefinida')
	return

def ttl_error():
	raise Exception('Error: pincel no esta definido o fue eliminado')
	return

def fig_error():
	raise Exception('Error: figura no esta definida o fue borrda')
	return

class VirtualMachine():
	def __init__(self):
		self.mem = Memory()
		self.shapes = []

	def run_list(self, caller, canvas, quad_list):
		self.caller = caller
		self.canvas = canvas
		self.quad_list = quad_list

		caller.print('Output: ')
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


		'''
		DONT REMOVE THIS TURTLE IT SETS THE POS(0,0) AS THE CENTERS AND 
		IF WE DONT HAVE IT ALL THE TKINTER FIGURES GET REMOVED'''
		ttl = turtle.RawTurtle(self.canvas)
		ttl.color('#fff')
		'''
		DONT REMOVE ABOVE TURTLE
		'''
		
		while ip < len(self.quad_list):
			quad = self.quad_list[ip]

			if len(str(quad.o1)) > 0 and str(quad.o1)[0] == '*':
				quad.o1 = self.mem.getValue(int(quad.o1[1:]))
			if len(str(quad.o2)) > 0 and str(quad.o2)[0] == '*':
				quad.o2 = self.mem.getValue(int(quad.o2[1:]))
			if len(str(quad.res)) > 0 and str(quad.res)[0] == '*':
				quad.res = self.mem.getValue(int(quad.res[1:]))

			if quad.action == PRINT:
				printable_obj = self.mem.getValue(int(quad.res))

				if printable_obj is None:
					printUndefinedValue()
					return

				if (printable_obj == TRUE):
					caller.print('verdadero')
				elif (printable_obj == FALSE):
					caller.print('falso')
				else:
					caller.print(printable_obj)

			elif quad.action == READ:
				if quad.res < 9000:
					caller.print('error Lectura')
					return

				elif quad.res >= 9000 and quad.res < 10000:
					self.caller.insert_prompt()

					while self.caller.receiving_input:
						pass

					bRes = self.caller.input

					if bRes == 'verdadero':
						TempMemory.setValue(int(quad.res), TRUE)

					elif bRes == 'falso':
						TempMemory.setValue(int(quad.res), FALSE)

					else:
						caller.print("Eso no es un bool")
						return

				elif quad.res >= 10000 and quad.res < 11000:
					try:
						self.caller.insert_prompt()

						while self.caller.receiving_input:
							pass

						iRes = self.caller.input

						TempMemory.setValue(int(quad.res), int(iRes))
					except ValueError:
						caller.print("Eso no es un entero")
						return

				elif quad.res >= 11000 and quad.res < 12000:
					try:
						self.caller.insert_prompt()

						while self.caller.receiving_input:
							pass

						fRes = self.caller.input

						TempMemory.setValue(int(quad.res), float(fRes))
					except ValueError:
						caller.print("Eso no es un decimal")
						return

				elif quad.res >= 12000 and quad.res < 13000:
					self.caller.insert_prompt()

					while self.caller.receiving_input:
						pass

					sRes = self.caller.input
					TempMemory.setValue(int(quad.res), str(sRes))

				else:
					caller.print('error lectura')
					return

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
					caller.print('Error: variable indefinida')
					return

				if bool_res == FALSE:
					ip = int(quad.res) - 1
				else:
					pass

			elif quad.action == VERIFY:
				quad_o1 = self.mem.getValue(int(quad.o1))

				if int(quad_o1) >= int(quad.o2) and int(quad_o1) <= int(quad.res):
					pass
				else:
					caller.print('Error: Indice fuera de limites de arreglo')

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
						caller.print(self.mem.getValue(int(quad.o1)))

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

			#PINCEL
						
			elif quad.action == P_COL:
				#quad in the form action -> ttl address - ' ' - color address
				ttl = self.mem.getValue(int(quad.o1))
				if ttl == None:
					ttl_error()
				try:
					color = self.mem.getValue(int(quad.res))
					ttl.color(color)
				except:
					try:
						color = self.mem.getValue(int(quad.res))
						color = g.colorDict[color]
						ttl.color(color)
					except:
						color = self.mem.getValue(int(quad.res))
						raise Exception('Error: color : ' + color + ' no me sirve')
						return

			elif quad.action == P_GO:
				#quad in the form action -> ttl address - ' ' - move indicator address
				ttl = self.mem.getValue(int(quad.o1))
				if ttl == None:
					ttl_error()
				ttl.forward(self.mem.getValue(int(quad.res)))

			elif quad.action == P_ROT:
				#quad in the form action -> ttl address - ' ' - degree indicator address
				ttl = self.mem.getValue(int(quad.o1))
				degrees = self.mem.getValue(int(quad.res))
				if(degrees >= 0):
					ttl.right(degrees)
				else:
					degrees = degrees * -1
					ttl.left(degrees)

			elif quad.action == P_DIS:
				#quad in the form -> action - x address - y address - ttl address
				ttl = self.mem.getValue(int(quad.res))
				if ttl == None:
					ttl_error()
				x = self.mem.getValue(int(quad.o1))
				y = self.mem.getValue(int(quad.o2))

				ttl.penup()
				ttl.setposition(x, y)
				ttl.pendown()	

			elif quad.action == P_DEL:
				#quad in the form -> action - '' - '' - ttl address
				ttl = self.mem.getValue(int(quad.res))
				if ttl == None:
					ttl_error()

				ttl.ht()
				self.mem.setValue(None, int(quad.res))

			elif quad.action == P_THICK:
				#quad in the form action -> ttl address - ' ' - thick indicator address
				ttl = self.mem.getValue(int(quad.o1))
				if ttl == None:
					ttl_error()

				thickness = self.mem.getValue(int(quad.res))

				if(thickness < 0):
					raise Exception('Error: grosor ' + str(thickness) + ' no puede ser negativo')
					return

				ttl.width(thickness)

			elif quad.action == P_ARC:
				#quad in the form -> action - x address - y address - ttl address
				ttl = self.mem.getValue(int(quad.res))
				if ttl == None:
					ttl_error()

				raise Exception('test')

				radius = self.mem.getValue(int(quad.o1))
				extent = self.mem.getValue(int(quad.o2))

				ttl.circle(radius, extent)

			# FIGURA
			elif quad.action == F_COL:
				#quad in the form action -> fig address - ' ' - color address
				fig = self.mem.getValue(int(quad.o1))
				if fig == None:
					fig_error()
				col = self.mem.getValue(int(quad.res))
				try:
					self.canvas.itemconfig(fig, fill=col)
				except:
					try:
						color = g.colorDict[col]
						self.canvas.itemconfig(fig, fill=color)
					except KeyError:
						print(g.colorDict[col])
						color = self.mem.getValue(int(quad.res))
						raise Exception('Error: color ' + col +' no me sirve')
						return

			elif quad.action == F_RMV:
				#quad in the form -> action - '' - '' - fig address
				fig = self.mem.getValue(int(quad.res))
				if fig == None:
					fig_error()

				self.canvas.delete(fig)
				self.mem.setValue(None, int(quad.res))

			elif quad.action == F_GRW:
				#quad in the form -> action - fig address - '' - scale
				fig = self.mem.getValue(int(quad.o1))
				scale = self.mem.getValue(int(quad.res))

				if scale < 0:
					raise Exception('Error: no puedo crecer a una escala menora a cero')

				if fig == None:
					fig_error()

				coords = self.canvas.coords(fig)
				new_coords = []

				for coord in coords:
					new_coords.append(coord * scale)

				if len(new_coords) == 4:
					self.canvas.coords(fig, new_coords[0], new_coords[1], new_coords[2], new_coords[3])

				if len(new_coords) == 6:
					self.canvas.coords(fig, new_coords[0], new_coords[1], new_coords[2], new_coords[3], new_coords[4], new_coords[5])

			elif quad.action == F_MVE:
				#quad in the form -> action - x address - y address - ttl address
				fig = self.mem.getValue(int(quad.res))
				if fig == None:
					fig_error()

				x = self.mem.getValue(int(quad.o1))
				y = self.mem.getValue(int(quad.o2))

				self.canvas.move(fig, x, y)

			ip += 1
			self.canvas.update()

		#self.frida_gui.mainloop()

	def drawBrush(self, fig_param_stack, res_address):

		color = self.mem.getValue(fig_param_stack.pop())

		# create a turtle object
		ttl = turtle.RawTurtle(self.canvas)
		
		try:
			ttl.color(color)
		except:
			try:
				color = g.colorDict[color]
				ttl.color(color)
			except KeyError:
				raise Exception('Error: color ' + color + ' no me sirve')
				return
			
		ttl.speed('fastest')
		ttl.shape('circle')

		self.mem.setValue(ttl, int(res_address))


	def drawShape(self, fig_code, fig_param_stack, res_address):

		color = self.mem.getValue(fig_param_stack.pop())
		pos_y = self.mem.getValue(fig_param_stack.pop())
		pos_x = self.mem.getValue(fig_param_stack.pop())
		fig = 0

		try:

			if fig_code == CUADRADO:
				sqr_len = self.mem.getValue(fig_param_stack.pop())
				try:
					fig = self.canvas.create_rectangle(pos_x, pos_y, pos_x + sqr_len, pos_y + sqr_len, fill = color)
				except:
					try:
						color = g.colorDict[color]
						fig = self.canvas.create_rectangle(pos_x, pos_y, pos_x + sqr_len, pos_y + sqr_len, fill = color)
					except:
						print('Error: color ' + color + ' no me sirve')
						sys.exit()

			elif fig_code == RECTANGULO:
				height = self.mem.getValue(fig_param_stack.pop())
				width = self.mem.getValue(fig_param_stack.pop())
				try:
					fig = self.canvas.create_rectangle(pos_x, pos_y, pos_x + width, pos_y + height, fill = color)
				except:
					try:
						color = g.colorDict[color]
						fig = self.canvas.create_rectangle(pos_x, pos_y, pos_x + width, pos_y + height, fill = color)
					except:
						print('Error: color ' + color + ' no me sirve')
						sys.exit()

			elif fig_code == CIRCULO:
				cir_di = self.mem.getValue(fig_param_stack.pop()) * 2
				try:
					fig = self.canvas.create_oval(pos_x, pos_y, pos_x + cir_di, pos_y + cir_di, fill = color)
				except:
					try:
						color = g.colorDict[color]
						fig = self.canvas.create_oval(pos_x, pos_y, pos_x + cir_di, pos_y + cir_di, fill = color)
					except:
						print('Error: color ' + color + ' no me sirve')
						sys.exit()

			elif fig_code == TRIANGULO:
				p3_y = pos_y
				p3_x = pos_x
				p2_y = self.mem.getValue(fig_param_stack.pop())
				p2_x = self.mem.getValue(fig_param_stack.pop())
				p1_y = self.mem.getValue(fig_param_stack.pop())
				p1_x = self.mem.getValue(fig_param_stack.pop())
				points = [p1_x, p1_y, p2_x, p2_y, p3_x, p3_y]
				try:
					fig = self.canvas.create_polygon(points, fill = color)
				except:
					try:
						color = g.colorDict[color]
						fig = self.canvas.create_polygon(points, fill = color)
					except:
						print('Error: color ' + color + ' no me sirve')
						sys.exit()

			self.mem.setValue(fig, int(res_address))

		except:
			raise Exception('Error: color ' + color + ' no me sirve')
			sys.exit()

	def relational_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if o1 is None or o2 is None:
			printUndefinedValue()
			return

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
		raise Exception('Error relacional')
		return

	def basic_math(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))		

		if o1 is None or o2 is None:
			raise Exception('Error: acceso a valor indefinido')
			return

		if action == SUM:
			return o1 + o2
		elif action == SUB:
			return o1 - o2
		elif action == MULT:
			return o1 * o2
		elif action == DIV:
			if o2 == 0:
				raise Exception('Error: Division entre 0')
			return o1 / o2
		raise Exception('Error matematico')
		return

	def logic_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if o1 is None or o2 is None:
			raise Exception('Error: acceso a valor indefinido')
			return

		o1 = True if o1 == TRUE else False
		o2 = True if o2 == TRUE else False

		if action == AND:
			return TRUE if o1 and o2 else FALSE
		elif action == OR:
			return TRUE if o1 or o2 else FALSE

		raise Exception('Error logica')
		return

