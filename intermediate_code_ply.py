from semantic_cube import *
from symbol_table import *
from quadruples import *
import global_vars as g
from memory import *
from dimension import *

def p_init_quad(p):
	'init_quad : empty'
	quad = QuadrupleItem(GOTO, '','','')
	Quadruple.add_quad(quad)

def p_push_operation(p):
	'push_operation : empty'
	opCode = getOperationCode(p[-1])
	g.operStack.append(opCode)

def p_logica_helper(p):
	'logica_helper : empty'
	if( len(g.operStack) > 0 ):
		if (g.operStack[-1] == getOperationCode('y') or g.operStack[-1] == getOperationCode('o')):
			quad_maker()

def p_expresion_helper(p):
	'expresion_helper : empty'
	if( len(g.operStack) > 0 ):
		if (g.operStack[-1] == getOperationCode('>') or g.operStack[-1] == getOperationCode('<') 
			or g.operStack[-1] == getOperationCode('>=') or g.operStack[-1] == getOperationCode('<=')
			or g.operStack[-1] == getOperationCode('==') or g.operStack[-1] == getOperationCode('!=')):
			quad_maker()

def p_exp_helper(p):
	'exp_helper : empty'

	if( len(g.operStack) > 0 ):
		if (g.operStack[-1] == getOperationCode('+') or g.operStack[-1] == getOperationCode('-')):
			quad_maker()

def p_factor_helper(p):
	'factor_helper : empty'
	if( len(g.operStack) > 0):
		if (g.operStack[-1] == getOperationCode('*') or g.operStack[-1] == getOperationCode('/')):
			quad_maker()

def p_push_fake_bottom(p):
	'push_fake_bottom : empty'
	opCode = getOperationCode(p[-1])
	g.operStack.append(opCode)
	
def p_pop_fake_bottom(p):
	'pop_fake_bottom : empty'
	g.operStack.pop()

def p_printQuadList(p):
	'printQuadList : empty'
	Quadruple.print_list()
	Quadruple.run_list()

def quad_maker():
	global i

	right_o = g.oStack.pop()
	right_type = g.typeStack.pop()

	left_o = g.oStack.pop()
	left_type = g.typeStack.pop()

	operand = g.operStack.pop()
	resultType = getResultType(left_type, operand, right_type)
	resType = ''
	
	if(resultType > 0):

		virtual_address = TempMemory.getAddress(resultType)

		quad = QuadrupleItem(operand, left_o, right_o, virtual_address)
		Quadruple.add_quad(quad)

		g.oStack.append(virtual_address)
		g.typeStack.append(resultType)

	else:
		print('Error: tipo no coincide')
		print(left_o + getOperationStr(operand) + right_o)
		print(getTypeStr(left_type) + getOperationStr(operand) + getTypeStr(right_type))
		sys.exit()

def push_o(p, type):
	resType = ''
	
	if type == 'var':
		resType = SymbolsTable.checkVarType(g.funcName, p)
	elif type == 'func':
		resType = SymbolsTable.checkFuncReturnType(p)
	else:
		resType = type

	resType = getTypeCode(resType)

	g.oStack.append(p)
	g.typeStack.append(resType)

def assign_helper():
	if( len(g.operStack) > 0):
		if (g.operStack[-1] == getOperationCode('=')):

			left_o = g.oStack.pop()
			res = g.oStack.pop()
			operand = g.operStack.pop()
			right_type = g.typeStack.pop()
			left_type = g.typeStack.pop()			
			resultType = getResultType(left_type, operand, right_type)

			if resultType > 0:
				quad = QuadrupleItem(operand, res, '' , left_o)
				Quadruple.add_quad(quad)
			else:
				print('No puedo asignar ' + str(res) + ' del tipo ' + getTypeStr(right_type) + ' a la variable ' + str(left_o) + ' por que es ' + getTypeStr(left_type))
				sys.exit()


def read_helper():
	address = TempMemory.getAddress(getTypeCode(g.nextType))
	opCode = getOperationCode('read')
	quad = QuadrupleItem(opCode, '' , '' ,address)
	Quadruple.add_quad(quad)
	g.oStack.append(address)
	g.typeStack.append(getTypeCode(g.nextType))

def print_helper():
	res = g.oStack.pop()
	opCode = getOperationCode('print')
	quad = QuadrupleItem(opCode, '' , '' ,res)
	Quadruple.add_quad(quad)

# Inflection points
def p_if_1(p):
	'if_1 : empty'
	exp_type = g.typeStack.pop()

	if (exp_type != getTypeCode('bool')):
		print('Error: tipo no coincide')
		print('Esperaba bool pero me diste un ' + getTypeStr(exp_type))
		sys.exit()
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

	if exp_type != getTypeCode('bool'):
		print('Error: tipo no coincide')
		print('Esperaba bool pero me diste un ' + getTypeStr(exp_type))
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

def p_check_return(p):
	'check_return : empty'
	ret_type = SymbolsTable.checkFuncReturnType(g.funcName)

	if ret_type == 'void':
		print('Error: funcion ' + g.funcName + ' de tipo void no puede tener estatuto de retorno')
		sys.exit()
	else:
		g.funcHasReturn = True

		ret_type = SymbolsTable.checkFuncReturnType(g.funcName)

		res = g.oStack.pop()
		act_type = g.typeStack.pop()

		func_result = getResultType(getTypeCode(ret_type), getOperationCode('return'), act_type)

		if func_result > 0:
			quad = QuadrupleItem(RET, '', '', res)
			Quadruple.add_quad(quad)
			g.typeStack.append(func_result)
		else:
			print('Error: funcion ' + g.funcName + ' de tipo '+ g.funcType +' no puede regresar valor de tipo ' + getTypeStr(act_type))
			sys.exit()

def p_gen_end_proc(p):
	'gen_end_proc : empty'

	ret_type = SymbolsTable.checkFuncReturnType(g.funcName)
	if ret_type != 'void' and g.funcHasReturn == False:
		print('Error: funcion ' + g.funcName + ' de tipo ' + g.funcType + ' no tiene estatuto de retorno')
		sys.exit()
	else:
		g.funcHasReturn = False

	quad = QuadrupleItem(ENDPROC, '', '', '')
	Quadruple.add_quad(quad)
