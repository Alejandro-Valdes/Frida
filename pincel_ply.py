from semantic_cube import *
from symbol_table import *
from quadruples import *
import global_vars as g
from memory import *
from dimension import *

def p_pincel_color(p):
	'pincel_color : empty'

	"""Valida que último operando sea cadena y agrega cuádruplo
	para cambiar el color del pincel.
	"""

	address = SymbolsTable.checkVarAddress(g.funcName, g.fig_name)
	res_type = g.typeStack.pop()
	color = g.oStack.pop()

	if(res_type != CADENA):
		print('ERROR: para cambiar el color necesito una cadena')
		return

	quad = QuadrupleItem(P_COL, address, '', color)
	Quadruple.add_quad(quad)

# Move brush forward
def p_pincel_paint(p):
	'pincel_paint : empty'

	"""Crea cuádruplo que mueve pincel un número de pasos
	determinado por la última expresión en la pila de operandos
	"""

	address = SymbolsTable.checkVarAddress( g.funcName, g.fig_name)
	res_type = g.typeStack.pop()
	steps = g.oStack.pop()
	
	if(res_type != ENTERO and res_type != DECIMAL):
		print('ERROR: para moverme necesito una numero')
		return

	quad = QuadrupleItem(P_GO, address, '', steps)
	Quadruple.add_quad(quad)

def p_pincel_rotate(p):
	'pincel_rotate : empty'

	"""Crea cuádruplo para rotar el pincel un número de grados 
	determinado por la última expresión en la pila de operandos
	"""

	address = SymbolsTable.checkVarAddress( g.funcName, g.fig_name)
	res_type = g.typeStack.pop()

	degrees = g.oStack.pop()
	
	if(res_type != ENTERO and res_type != DECIMAL):
		print('ERROR: para girar necesito una numero')
		return

	quad = QuadrupleItem(P_ROT, address, '', degrees)
	Quadruple.add_quad(quad)

def p_pincel_displace(p):
	'pincel_displace : empty'

	"""Crea cuádruplo para desplaza el pincel un número de pasos 
	determinado por la última expresión en la pila de operandos
	"""

	address = SymbolsTable.checkVarAddress(g.funcName, g.fig_name)
	res_y = g.typeStack.pop()
	y = g.oStack.pop()

	res_x = g.typeStack.pop()
	x = g.oStack.pop()
	
	if(res_x != ENTERO or res_y != ENTERO):
		print('ERROR: para desplazarme necesito una cordenada (x,y) de enteros')
		return

	quad = QuadrupleItem(P_DIS, x, y, address)
	Quadruple.add_quad(quad)

def p_pincel_thickness(p):
	'pincel_thickness : empty'

	"""Crea cuádruplo para cambiar el grosor del pincel 
	a razón del top de la pila de operandos.
	"""

	address = SymbolsTable.checkVarAddress( g.funcName, g.fig_name)
	res_type = g.typeStack.pop()

	thick = g.oStack.pop()
	
	if(res_type != ENTERO and res_type != DECIMAL):
		print('ERROR: para crecer necesito una numero')
		return

	quad = QuadrupleItem(P_THICK, address, '', thick)
	Quadruple.add_quad(quad)

def p_pincel_remove(p):
	'pincel_remove : empty'

	"""Crea cuádruplo para borrar un pincel
	"""

	address = SymbolsTable.checkVarAddress( g.funcName, g.fig_name)
	
	quad = QuadrupleItem(P_DEL, '', '', address)
	Quadruple.add_quad(quad)

def p_pincel_arc(p):
	'pincel_arc : empty'

	"""Crea cuádruplo para dibujar un arco con tamaño determinado 
	por el último valor en la pila de operandos y radio determinado 
	por el penúltimo valor en la pilda de operandos."""

	address = SymbolsTable.checkVarAddress( g.funcName, g.fig_name)

	res_extent = g.typeStack.pop()
	extent = g.oStack.pop()

	res_radius = g.typeStack.pop()
	radius = g.oStack.pop()

	if(res_extent != ENTERO and res_extent != DECIMAL and res_radius != ENTERO and res_radius != DECIMAL):
		print('ERROR: para arco necesito dos numeros, un radio y una longitud')
		return

	quad = QuadrupleItem(P_ARC, radius, extent, address)
	Quadruple.add_quad(quad)
