from semantic_cube import getResultType
from symbol_table import *
from quadruples import *
import global_vars as g

i = 0;

GOTO = 'GoTo'
GOTOV = 'GoToV'
GOTOF = 'GoToF'
ENDPROC = 'return'

def p_push_operation(p):
	'push_operation : empty'
	g.operStack.append(p[-1])

def p_logica_helper(p):
	'logica_helper : empty'
	if( len(g.operStack) > 0 ):
		if (g.operStack[-1] == 'y' or g.operStack[-1] == 'o'):
			quad_maker()

def p_expresion_helper(p):
	'expresion_helper : empty'
	if( len(g.operStack) > 0 ):
		if (g.operStack[-1] == '>' or g.operStack[-1] == '<' 
			or g.operStack[-1] == '>=' or g.operStack[-1] == '<='
			or g.operStack[-1] == '==' or g.operStack[-1] == '!='):
			quad_maker()

def p_exp_helper(p):
	'exp_helper : empty'

	if( len(g.operStack) > 0 ):
		if (g.operStack[-1] == '+' or g.operStack[-1] == '-'):
			quad_maker()

def p_factor_helper(p):
	'factor_helper : empty'
	if( len(g.operStack) > 0):
		if (g.operStack[-1] == '*' or g.operStack[-1] == '/'):
			quad_maker()

def p_push_fake_bottom(p):
	'push_fake_bottom : empty'
	g.operStack.append(p[-1])
	
def p_pop_fake_bottom(p):
	'pop_fake_bottom : empty'
	g.operStack.pop()

def p_printQuadList(p):
	'printQuadList : empty'
	Quadruple.print_list()

def quad_maker():
	global i
	right_o = g.oStack.pop()
	right_type = g.typeStack.pop()
	left_o = g.oStack.pop()
	left_type = g.typeStack.pop()
	operand = g.operStack.pop()
	resultType = getResultType(right_type+operand+left_type)
	resType = ''

	if(resultType > 0):
		res = 't' + str(i)
		quad = QuadrupleItem(operand, left_o, right_o, res)
		Quadruple.add_quad(quad)

		g.oStack.append(res)

		if(resultType == 1):
			resType = 'bool'
		elif(resultType == 2):
			resType = 'entero'
		elif(resultType == 3):
			resType = 'decimal'
		elif(resultType == 4):
			resType = 'cadena'

		g.typeStack.append(resType)

		i+=1
	else:
		print('Error type mismatch')
		print(operand + left_o + right_o)
		sys.exit()

def push_o(p, type):
	resType = ''

	if type == 'var':
		resType = SymbolsTable.checkVarType(g.funcName, p)
	elif type == 'func':
		resType = SymbolsTable.checkFuncReturnType(p)
	else:
		resType = type

	g.oStack.append(p)
	g.typeStack.append(resType)

def assign_helper():
	if( len(g.operStack) > 0):
		if (g.operStack[-1] == '='):
			left_o = g.oStack.pop()
			res = g.oStack.pop()
			operand = g.operStack.pop()
			quad = QuadrupleItem(operand, res, '' , left_o)
			Quadruple.add_quad(quad)

def read_helper():
	global i
	res = 't' + str(i)
	quad = QuadrupleItem('leer', '' , '' ,res)
	Quadruple.add_quad(quad)
	g.oStack.append(res)
	i += 1

def print_helper():
	res = g.oStack.pop()
	quad = QuadrupleItem('imprimir', '' , '' ,res)
	Quadruple.add_quad(quad)

# Inflection points
def p_if_1(p):
	'if_1 : empty'
	exp_type = g.typeStack.pop()
	if (exp_type != 'bool'):
		print('ERROR: Type mismatch!')
	else:
		res = g.oStack.pop()
		quad = QuadrupleItem(GOTOF, res, '', '')
		Quadruple.add_quad(quad)
		cont = len(Quadruple.quadruple_list)
		g.jumpStack.append(cont - 1)

# TODO: ELIF

def p_cond_floor(p):
	'cond_floor : empty'
	g.jumpStack.append(-1)

def p_if_2(p):
	'if_2 : empty'
	cont = len(Quadruple.quadruple_list)
	end = g.jumpStack.pop()
	while end > 0:
		Quadruple.quadruple_list[end].res = str(cont)
		end = g.jumpStack.pop()


def p_if_else_3(p):
	'if_else_3 : empty'
	quad = QuadrupleItem(GOTO, '', '', '')
	Quadruple.add_quad(quad)
	false = g.jumpStack.pop()
	cont = len(Quadruple.quadruple_list)
	g.jumpStack.append(cont - 1)
	Quadruple.quadruple_list[false].res = str(cont) 

def p_while_1(p):
	'while_1 : empty'
	cont = len(Quadruple.quadruple_list)
	g.jumpStack.append(cont)

def p_while_2(p):
	'while_2 : empty'
	exp_type = g.typeStack.pop()
	if exp_type != 'bool':
		print('Error type mismatch')
		print('expected bool but got ' + exp_type)
		sys.exit()
	else:
		result = g.oStack.pop()
		quad = QuadrupleItem(GOTOF, str(result), '', '')
		Quadruple.add_quad(quad)

		cont = len(Quadruple.quadruple_list)
		g.jumpStack.append(cont-1)


def p_while_3(p):
	'while_3 : empty'	
	end = g.jumpStack.pop()
	ret = g.jumpStack.pop()
	quad = QuadrupleItem(GOTO, '', '', str(ret))
	Quadruple.add_quad(quad)
	cont = len(Quadruple.quadruple_list)
	Quadruple.quadruple_list[end].res = str(cont)

def p_gen_end_proc(p):
	'gen_end_proc : empty'

	quad = QuadrupleItem(ENDPROC, '', '', '')
	Quadruple.add_quad(quad)
