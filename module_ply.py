from semantic_cube import *
from symbol_table import *
from quadruples import *
import global_vars as g

def p_mod_call_2(p):
	'mod_call_2 : empty'
	name = g.funcExpName
	quad = QuadrupleItem(ERA, name, '' ,'')

	if(len(g.funcExpNameStack) > 0):
		g.funcExpName = g.funcExpNameStack.pop()

	Quadruple.add_quad(quad)
	g.param_count = 0

def p_mod_call_3(p):
	'mod_call_3 : empty'
	arg = g.oStack.pop()
	arg_type = g.typeStack.pop()
	expected_type = SymbolsTable.check_param(g.funcExpName, g.param_count)
	
	semantic_res = getResultType(getTypeCode(expected_type), PARAM, arg_type);

	if arg_type != getTypeCode(expected_type) and semantic_res == -1 :
		raise Exception('Error: funcion ' + g.funcExpName+ ' esperaba ' + expected_type + ' pero me mandaste ' + getTypeStr(arg_type))

	quad = QuadrupleItem(PARAM, arg , '', 'param' + str(g.param_count+1))

	Quadruple.add_quad(quad)

def p_mod_call_4(p):
	'mod_call_4 : empty'
	g.param_count += 1

	if g.param_count + 1 > SymbolsTable.params_size(g.funcExpName):
		raise Exception('Error: Le mandaste parametros de mas a la funcion ' + g.funcExpName)

def p_mod_call_5(p):
	'mod_call_5 : empty'

	act_param_size = g.param_count + 1
	expected_param_size = SymbolsTable.params_size(g.funcExpName)

	if act_param_size == expected_param_size:
		pass

	elif act_param_size < expected_param_size:
		raise Exception('Error: Le mandaste parametros de mas a la funcion ' + g.funcExpName)

def p_mod_call_6(p):
	'mod_call_6 : empty'

	quadPointer = SymbolsTable.getFuncPI(g.funcExpName)
	quad = QuadrupleItem(GOSUB, g.funcExpName, '' , str(quadPointer))

	Quadruple.add_quad(quad)

	


def p_mod_call_empty(p):
	'mod_call_empty : empty'
	expected_param_size = SymbolsTable.params_size(g.funcExpName)
	if expected_param_size > 0:
		raise Exception('Error: No le mandaste nada a la funcion ' + g.funcExpName)



