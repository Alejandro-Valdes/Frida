from semantic_cube import *
from symbol_table import *
from quadruples import *
import global_vars as g
from memory import *
from dimension import *

def p_pincel_color(p):
	'pincel_color : empty'
	address = SymbolsTable.checkVarAddress( g.funcName, g.actualVarObj.name)
	res_type = g.typeStack.pop()
	color = g.oStack.pop()

	if(res_type != CADENA):
		print('ERROR: para cambiar el color necesito una cadena')
		sys.exit()

	quad = QuadrupleItem(P_COL, address, '', color)
	Quadruple.add_quad(quad)

# Move brush forward
def p_pincel_paint(p):
	'pincel_paint : empty'
	address = SymbolsTable.checkVarAddress( g.funcName, g.actualVarObj.name)
	res_type = g.typeStack.pop()

	steps = g.oStack.pop()
	
	if(res_type != ENTERO and res_type != DECIMAL):
		print('ERROR: para moverme necesito una numero')
		sys.exit()

	quad = QuadrupleItem(P_GO, address, '', steps)
	Quadruple.add_quad(quad)

def p_pincel_rotate(p):
	'pincel_rotate : empty'
	address = SymbolsTable.checkVarAddress( g.funcName, g.actualVarObj.name)
	res_type = g.typeStack.pop()

	degrees = g.oStack.pop()
	
	if(res_type != ENTERO and res_type != DECIMAL):
		print('ERROR: para girar necesito una numero')
		sys.exit()

	quad = QuadrupleItem(P_ROT, address, '', degrees)
	Quadruple.add_quad(quad)

def p_pincel_displace(p):
	'pincel_displace : empty'
	address = SymbolsTable.checkVarAddress(g.funcName, g.actualVarObj.name)
	res_x = g.typeStack.pop()
	x = g.oStack.pop()

	res_y = g.typeStack.pop()
	y = g.oStack.pop()
	
	if(res_x != ENTERO or res_y != ENTERO):
		print('ERROR: para desplazarme necesito una cordenada (x,y) de enteros')
		sys.exit()

	quad = QuadrupleItem(P_DIS, x, y, address)
	Quadruple.add_quad(quad)
