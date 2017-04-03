from semantic_cube import getResultType
from symbol_table import *
from quadruples import *
import global_vars as g

global name

def p_mod_call_2(p):
	'mod_call_2 : empty'
	global name
	# p-3 to get func name
	name = p[-3]
	quad = QuadrupleItem('era', name, '' ,'')
	Quadruple.add_quad(quad)
	g.param_count = 0

def p_mod_call_3(p):
	'mod_call_3 : empty'
	global name
	arg = g.oStack.pop()
	arg_type = g.typeStack.pop()
	expected_type = SymbolsTable.check_param(name, g.param_count)

	if arg_type != expected_type:
		print('Type mismatch: expected '+ expected_type + ' but got ' + arg_type)
		sys.exit()

	quad = QuadrupleItem('param', arg , '', 'param' + str(g.param_count+1))
	Quadruple.add_quad(quad)

def p_mod_call_4(p):
	'mod_call_4 : empty'
	g.param_count += 1

	if g.param_count + 1 > SymbolsTable.params_size(name):
		print('error: way to many parameters for function ' + name)
		sys.exit()

def p_mod_call_5(p):
	'mod_call_5 : empty'

	act_param_size = g.param_count + 1
	expected_param_size = SymbolsTable.params_size(name)

	if act_param_size == expected_param_size:
		pass

	elif act_param_size < expected_param_size:
		print('error: way to few parameters for function ' + name)
		sys.exit()

def p_mod_call_6(p):
	'mod_call_6 : empty'
	global name
	quadPointer = SymbolsTable.getFuncPI(name)
	quad = QuadrupleItem('gosub', name, '' , str(quadPointer))
	Quadruple.add_quad(quad)


def p_mod_call_empty(p):
	'mod_call_empty : empty'
	expected_param_size = SymbolsTable.params_size(name)
	if expected_param_size > 0:
		print('error: missing all parameters for function ' + name)
		sys.exit()



