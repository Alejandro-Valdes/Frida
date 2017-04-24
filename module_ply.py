from semantic_cube import *
from symbol_table import *
from quadruples import *
import global_vars as g

def p_mod_call_2(p):
	'mod_call_2 : empty'
	name = g.funcExpName
	quad = QuadrupleItem(ERA, Operand(name), Operand('') ,'')
	Quadruple.add_quad(quad)
	g.param_count = 0

def p_mod_call_3(p):
	'mod_call_3 : empty'
	arg = g.oStack.pop()
	arg_type = g.typeStack.pop()
	expected_type = SymbolsTable.check_param(g.funcExpName, g.param_count)
	print (arg)
	print (arg_type)

	if arg_type != getTypeCode(expected_type):
		print('Error: Funcion ' + g.funcExpName + ' esperaba parametro de tipo '+ expected_type + ' pero me diste ' + getTypeStr(arg_type))
		sys.exit()

	quad = QuadrupleItem(PARAM, Operand(arg) , Operand(''), 'param' + str(g.param_count+1))
	Quadruple.add_quad(quad)

def p_mod_call_4(p):
	'mod_call_4 : empty'
	g.param_count += 1

	if g.param_count + 1 > SymbolsTable.params_size(g.funcExpName):
		print('Error: Le mandaste parametros de mas a la funcion ' + g.funcExpName)
		sys.exit()

def p_mod_call_5(p):
	'mod_call_5 : empty'

	act_param_size = g.param_count + 1
	expected_param_size = SymbolsTable.params_size(g.funcExpName)

	if act_param_size == expected_param_size:
		pass

	elif act_param_size < expected_param_size:
		print('Error: Le mandaste muy poquitos parametros a la funcion ' + g.funcExpName)
		sys.exit()

def p_mod_call_6(p):
	'mod_call_6 : empty'
	quadPointer = SymbolsTable.getFuncPI(g.funcExpName)
	quad = QuadrupleItem(GOSUB, Operand(g.funcExpName), Operand('') , str(quadPointer))
	Quadruple.add_quad(quad)


def p_mod_call_empty(p):
	'mod_call_empty : empty'
	expected_param_size = SymbolsTable.params_size(g.funcExpName)
	if expected_param_size > 0:
		print('Error: No le mandaste nada a la funcion ' + g.funcExpName)
		sys.exit()



