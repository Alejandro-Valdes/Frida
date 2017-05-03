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

class VirtualMachine():
	def __init__(self):
		self.mem = Memory()
		self.shapes = []

	def run_list(self, caller, canvas, quad_list):
		self.caller = caller
		self.canvas = canvas
		self.quad_list = quad_list

		self.caller.print('Output: ')
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
		
		while ip < len(self.quad_list) and self.caller.running:

			quad = self.quad_list[ip]

			if len(str(quad.o1)) > 0 and str(quad.o1)[0] == '*':
				quad_o1 = self.mem.getValue(int(quad.o1[1:]))
			else:
				quad_o1 = quad.o1

			if len(str(quad.o2)) > 0 and str(quad.o2)[0] == '*':
				quad_o2 = self.mem.getValue(int(quad.o2[1:]))
			else:
				quad_o2 = quad.o2

			if len(str(quad.res)) > 0 and str(quad.res)[0] == '*':
				quad_res = self.mem.getValue(int(quad.res[1:]))
			else: 
				quad_res = quad.res

			if quad.action == PRINT:
				printable_obj = self.mem.getValue(int(quad_res))

				if printable_obj is None:
					printUndefinedValue()
					self.caller.running = False

				if (printable_obj == TRUE):
					self.caller.print('verdadero')
				elif (printable_obj == FALSE):
					self.caller.print('falso')
				else:
					self.caller.print(printable_obj)

			elif quad.action == READ:
				if quad_res < 9000:
					self.caller.print('error Lectura')
					self.caller.running = False

				elif quad_res >= 9000 and quad_res < 10000:
					self.caller.insert_prompt()

					self.caller.lock.acquire()

					bRes = self.caller.input

					if bRes == 'verdadero':
						TempMemory.setValue(int(quad_res), TRUE)

					elif bRes == 'falso':
						TempMemory.setValue(int(quad_res), FALSE)

					else:
						self.caller.print("Eso no es un bool")
						return

				elif quad_res >= 10000 and quad_res < 11000:
					try:
						self.caller.insert_prompt()

						self.caller.lock.acquire()

						iRes = self.caller.input

						TempMemory.setValue(int(quad_res), int(iRes))
					except ValueError:
						self.caller.print("Eso no es un entero")
						self.caller.running = False

				elif quad_res >= 11000 and quad_res < 12000:
					try:
						self.caller.insert_prompt()

						self.caller.lock.acquire()

						fRes = self.caller.input

						TempMemory.setValue(int(quad_res), float(fRes))
					except ValueError:
						self.caller.print("Eso no es un decimal")
						self.caller.running = False

				elif quad_res >= 12000 and quad_res < 13000:
					self.caller.insert_prompt()

					self.caller.lock.acquire()

					sRes = self.caller.input
					TempMemory.setValue(int(quad_res), str(sRes))

				else:
					self.caller.print('error lectura')
					self.caller.running = False

			elif quad.action == ASSIGN:
				res = self.mem.getValue(int(quad_o1))
				self.mem.setValue(res, int(quad_res))

			elif quad.action > RELSTART and quad.action < RELEND:
				res = self.relational_operation(quad.action, quad_o1, quad_o2)
				self.mem.setValue(res, int(quad_res))

			elif quad.action > MATHSTART and quad.action < MATHEND:
				res = self.basic_math(quad.action, quad_o1, quad_o2)
				self.mem.setValue(res, int(quad_res))

			elif quad.action == GOTO:
				ip = int(quad_res) - 1

			elif quad.action == GOTOF:
				bool_res = self.mem.getValue(int(quad_o1))
				if bool_res is None:
					self.caller.print('Error: variable indefinida')
					self.caller.print("%s %s" % (int(quad_o1), ip))
					self.caller.running = False

				if bool_res == FALSE:
					ip = int(quad_res) - 1
				else:
					pass

			elif quad.action == VERIFY:
				quad_o1 = self.mem.getValue(int(quad_o1))

				if int(quad_o1) >= int(quad_o2) and int(quad_o1) <= int(quad_res):
					pass
				else:
					self.caller.print('Error: Indice fuera de limites de arreglo')
					self.caller.running = False

			elif quad.action > ANDORSTART and quad.action < ANDOREND:
				res = self.logic_operation(quad.action, quad_o1, quad_o2)
				self.mem.setValue(res, int(quad_res))

			elif quad.action == ERA:
				paramAddresses = SymbolsTable.get_function_params_addresses(quad_o1)	

				#get memory that will be saved after the return or endproc	

				scoped_addresses = SymbolsTable.getScopedMemory(curr_scope)

				for address in scoped_addresses:
					temp_local_mem[int(address)] = self.mem.getValue(int(address))

				memory_stack.append(dict(temp_local_mem))
				memory_to_save.append(SymbolsTable.checkVarAddress(curr_scope, quad_o1))

			elif quad.action == GOSUB:
				ip_exe_stack.append(ip)
				ip = int(quad_res) - 1
				currParam = 0
				curr_scope = str(quad_o1)


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
				if int(quad_o1) in temp_local_mem:
					value = temp_local_mem[int(quad_o1)]
					if value is None:
						print (temp_local_mem)
						self.caller.print(self.mem.getValue(int(quad_o1)))

				else:
					value = self.mem.getValue(int(quad_o1))

				self.mem.setValue(value, int(paramAddresses[currParam]))
				currParam += 1

			elif quad.action == RET:
				resMem = quad_res
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
				fig_code = quad_o1

			elif quad.action == F_PAR:
				fig_param_stack.append(int(quad_res))

			elif quad.action == F_FIN:

				if fig_code == PINCEL:
					self.drawBrush(fig_param_stack, quad_res)

				else:
					self.drawShape(fig_code, fig_param_stack, quad_res)

			#PINCEL
						
			elif quad.action == P_COL:
				#quad in the form action -> ttl address - ' ' - color address
				ttl = self.mem.getValue(int(quad_o1))
				if ttl == None:
					ttl_error()
				try:
					color = self.mem.getValue(int(quad_res))
					color = g.colorDict[color]
					ttl.color(color)
				except Exception:
					color = self.mem.getValue(int(quad_res))

					self.caller.print('Error: color : ' + color + ' no me sirve')
					self.caller.running = False

			elif quad.action == P_GO:
				#quad in the form action -> ttl address - ' ' - move indicator address
				ttl = self.mem.getValue(int(quad_o1))
				if ttl == None:
					ttl_error()
				ttl.forward(self.mem.getValue(int(quad_res)))

			elif quad.action == P_ROT:
				#quad in the form action -> ttl address - ' ' - degree indicator address
				ttl = self.mem.getValue(int(quad_o1))
				degrees = self.mem.getValue(int(quad_res))
				if(degrees >= 0):
					ttl.right(degrees)
				else:
					degrees = degrees * -1
					ttl.left(degrees)

			elif quad.action == P_DIS:
				#quad in the form -> action - x address - y address - ttl address
				ttl = self.mem.getValue(int(quad_res))
				if ttl == None:
					ttl_error()
				x = self.mem.getValue(int(quad_o1))
				y = self.mem.getValue(int(quad_o2))

				ttl.penup()
				ttl.setposition(x, y)
				ttl.pendown()	

			elif quad.action == P_DEL:
				#quad in the form -> action - '' - '' - ttl address
				ttl = self.mem.getValue(int(quad_res))
				if ttl == None:
					ttl_error()

				ttl.ht()
				self.mem.setValue(None, int(quad_res))

			elif quad.action == P_THICK:
				#quad in the form action -> ttl address - ' ' - thick indicator address
				ttl = self.mem.getValue(int(quad_o1))
				if ttl == None:
					ttl_error()

				thickness = self.mem.getValue(int(quad_res))

				if(thickness < 0):
					self.caller.print('Error: grosor ' + str(thickness) + ' no puede ser negativo')
					self.caller.running = False

				ttl.width(thickness)

			elif quad.action == P_ARC:
				#quad in the form -> action - x address - y address - ttl address
				ttl = self.mem.getValue(int(quad_res))
				if ttl == None:
					ttl_error()

				self.caller.print('test')

				radius = self.mem.getValue(int(quad_o1))
				extent = self.mem.getValue(int(quad_o2))

				ttl.circle(radius, extent)

			# FIGURA
			elif quad.action == F_COL:
				#quad in the form action -> fig address - ' ' - color address
				fig = self.mem.getValue(int(quad_o1))
				if fig == None:
					fig_error()
				col = self.mem.getValue(int(quad_res))
				try:
					self.canvas.itemconfig(fig, fill=col)
				except:
					try:
						color = g.colorDict[col]
						self.canvas.itemconfig(fig, fill=color)
					except KeyError:
						print(g.colorDict[col])
						color = self.mem.getValue(int(quad_res))
						self.caller.print('Error: color ' + col +' no me sirve')
						self.caller.running = False

			elif quad.action == F_RMV:
				#quad in the form -> action - '' - '' - fig address
				fig = self.mem.getValue(int(quad_res))
				if fig == None:
					fig_error()

				self.canvas.delete(fig)
				self.mem.setValue(None, int(quad_res))

			elif quad.action == F_GRW:
				#quad in the form -> action - fig address - '' - scale
				fig = self.mem.getValue(int(quad_o1))
				scale = self.mem.getValue(int(quad_res))

				if scale < 0:
					self.caller.print('Error: no puedo crecer a una escala menor a cero')
					self.caller.running = False

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
				fig = self.mem.getValue(int(quad_res))
				if fig == None:
					fig_error()

				x = self.mem.getValue(int(quad_o1))
				y = self.mem.getValue(int(quad_o2))

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
				self.caller.print('Error: color ' + color + ' no me sirve')
				self.caller.running = False
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
						self.caller.running = False
						return

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
						self.caller.running = False
						return

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
						self.caller.running = False
						return

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
						self.caller.print('Error: color ' + color + ' no me sirve')
						self.caller.running = False
						return

			self.mem.setValue(fig, int(res_address))

		except:
			self.caller.print('Error: color ' + color + ' no me sirve')
			self.caller.running = False
			return

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
		self.caller.print('Error relacional')
		self.caller.running = False

	def basic_math(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))	

		if o1 is None or o2 is None:
			self.caller.print('Error: acceso a valor indefinido')
			self.caller.running = False
			return

		if action == SUM:
			return o1 + o2
		elif action == SUB:
			return o1 - o2
		elif action == MULT:
			return o1 * o2
		elif action == DIV:
			if o2 == 0:
				self.caller.print('Error: Division entre 0')
				self.caller.running = False
				return
			return o1 / o2
		self.caller.print('Error matematico')
		self.caller.running = False

	def logic_operation(self, action, o1, o2):
		o1 = self.mem.getValue(int(o1))
		o2 = self.mem.getValue(int(o2))

		if o1 is None or o2 is None:
			self.caller.print('Error: acceso a valor indefinido')
			self.caller.running = False
			return

		o1 = True if o1 == TRUE else False
		o2 = True if o2 == TRUE else False

		if action == AND:
			return TRUE if o1 and o2 else FALSE
		elif action == OR:
			return TRUE if o1 or o2 else FALSE

		self.caller.print('Error logica')
		self.caller.running = False
		return

	def printUndefinedValue(self):
		self.caller.print('Error: Acceso a variable indefinida')
		self.caller.running = False
		return

	def ttl_error(self):
		self.caller.print('Error: pincel no esta definido o fue eliminado')
		self.caller.running = False
		return

	def fig_error(self):
		self.caller.print('Error: figura no esta definida o fue borrda')
		self.caller.running = False
		return