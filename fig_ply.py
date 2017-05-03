from semantic_cube import *
from symbol_table import *
from quadruples import *
import global_vars as g
from memory import *
from dimension import *

def p_fig_move(p):
	'fig_move : empty'

	"""Regla fig_move utilizada para crear los cuádruplos de movimiento de una figura"""

	address = SymbolsTable.checkVarAddress(g.funcName, g.fig_name)

	# coordenada y
	res_y = g.typeStack.pop()
	y = g.oStack.pop() 

	# coordenada x
	res_x = g.typeStack.pop() 
	x = g.oStack.pop() 
	
	if(res_x != ENTERO or res_y != ENTERO):
		raise Exception('ERROR: para moverme necesito una cordenada (x,y) de enteros')

	quad = QuadrupleItem(F_MVE, x, y, address) 
	Quadruple.add_quad(quad)

def p_fig_grow(p):
	'fig_grow : empty'

	"""Regla fig_grow que crea los cuádruplos para escalar una figura"""

	address = SymbolsTable.checkVarAddress(g.funcName, g.fig_name)
	res_type = g.typeStack.pop()
	scale = g.oStack.pop()

	if(res_type != ENTERO and res_type != DECIMAL):
		raise Exception('ERROR: para crecer necesito un numero')

	quad = QuadrupleItem(F_GRW, address, '', scale)
	Quadruple.add_quad(quad)

def p_fig_fill(p):
	'fig_fill : empty'

	"""Regla fig_fill que crea los cuádruplos para Llenar una figura de un color"""

	address = SymbolsTable.checkVarAddress(g.funcName, g.fig_name)
	res_type = g.typeStack.pop()
	color = g.oStack.pop()

	if(res_type != CADENA):
		raise Exception('ERROR: para cambiar el color necesito una cadena')

	quad = QuadrupleItem(F_COL, address, '', color)
	Quadruple.add_quad(quad)

def p_fig_remove(p):
	'fig_remove : empty'

	"""Regla fig_remove que crea los cuádruplos para remover una figura del lienzo"""
	
	address = SymbolsTable.checkVarAddress( g.funcName, g.fig_name)
	
	quad = QuadrupleItem(F_RMV, '', '', address)
	Quadruple.add_quad(quad)