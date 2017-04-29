from semantic_cube import *
from symbol_table import *
from quadruples import *
import global_vars as g
from memory import *
from dimension import *

def p_init_quad(p):
	'init_quad : empty'
	quad = QuadrupleItem(GOTO, '', '', '')
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
		print(str(left_o) + getOperationStr(operand) + str(right_o))
		print(getTypeStr(left_type) + getOperationStr(operand) + getTypeStr(right_type))
		sys.exit()

def p_push_operand(p):
	'push_operand : empty'

	address = SymbolsTable.checkVarAddress(g.funcName, p[-2])
	if address > 0 and address != None:
		type = SymbolsTable.checkVarType(g.funcName, p[-2])
		push_o(str(address), type)

def push_o(p, type):
	resType = ''
	res = p
	
	if type == 'var':
		resType = SymbolsTable.checkVarType(g.funcName, p)
	elif type == 'func':
		resType = SymbolsTable.checkFuncReturnType(p)
		res = SymbolsTable.checkVarAddress(g.funcName, res)
	else:
		resType = type

	resType = getTypeCode(resType)

	g.oStack.append(res)
	g.typeStack.append(resType)

def assign_helper():
	if(len(g.operStack) > 0):
		if (g.operStack[-1] == getOperationCode('=')):

			left_o = g.oStack.pop()
			res = g.oStack.pop()
			operand = g.operStack.pop()
			right_type = g.typeStack.pop()
			left_type = g.typeStack.pop()			
			resultType = getResultType(left_type, operand, right_type)

			if resultType > 0:
				quad = QuadrupleItem(operand, res, '', left_o)
				Quadruple.add_quad(quad)
			else:
				print('No puedo asignar ' + str(res) + ' del tipo ' + getTypeStr(right_type) + ' a la variable ' + str(left_o) + ' por que es ' + getTypeStr(left_type))
				sys.exit()	

def read_helper():
	address = TempMemory.getAddress(getTypeCode(g.nextType))
	opCode = getOperationCode('read')
	quad = QuadrupleItem(opCode, '', '', address)
	Quadruple.add_quad(quad)
	g.oStack.append(address)
	g.typeStack.append(getTypeCode(g.nextType))

def print_helper():
	res = g.oStack.pop()
	type = g.typeStack.pop()
	opCode = getOperationCode('print')
	quad = QuadrupleItem(opCode, '', '',res)
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

def  p_save_fig(p):
	'save_fig : empty'
	g.fig_name = p[-1]

	quad = QuadrupleItem(FIG, getTypeCode(g.fig_name), '', '')

	Quadruple.add_quad(quad)

def p_push_fig_param(p):
	'push_fig_param : empty'
	arg = g.oStack.pop()
	arg_type = g.typeStack.pop()
	quad = QuadrupleItem(F_PAR, '', '', arg)
	Quadruple.add_quad(quad)

def p_fgra_fin(p):
	'fgra_fin : empty'
	address = SymbolsTable.checkVarAddress(g.funcName, g.varName)
	quad = QuadrupleItem(F_FIN, '', '', address)
	Quadruple.add_quad(quad)
	'''
	quad = QuadrupleItem(90000, address, '', address)

	Quadruple.add_quad(quad)
	'''



# -------- Arrays ----------

def p_init_array(p):
	'init_array : empty'

	address = SymbolsTable.checkVarAddress(g.funcName, g.varName)
	type = SymbolsTable.checkVarType(g.funcName, g.varName)
	push_o(str(address), type)

	if g.arrayBase == -1:
		g.arrayBase = g.oStack.pop()
		g.arrayType = g.typeStack.pop()

def p_assign_to_array(p):
	'assign_to_array : empty'

	if(len(g.operStack) > 0):
		if (g.operStack[-1] == getOperationCode('=')):

			last_val_mem = g.oStack.pop()
			operand = getOperationCode('=')
			right_type = g.typeStack.pop()
			resultType = getResultType(g.arrayType, operand, right_type)

			if resultType > 0:
				quad = QuadrupleItem(operand, last_val_mem, '', int(g.arrayBase) + g.arrayAssignmentCounter) 
				Quadruple.add_quad(quad)
				g.arrayAssignmentCounter += 1
			else:
				print('No puedo asignar ' + str(last_val_mem) + ' del tipo ' + getTypeStr(right_type) + ' a la variable ' + str(g.arrayBase) + ' por que es ' + getTypeStr(g.arrayType))
				sys.exit()	


def p_finish_array_assignment(p):
	'finish_array_assignment : empty'

	var = SymbolsTable.checkVariable(g.varName, g.funcName)

	if g.arrayAssignmentCounter != var.dimension_list.total_size:
		print('Error: Tamanio de asignacion no coincide con tamano de variable: ' + var.name)
		sys.exit()

	g.operStack.pop()
	g.arrayAssignmentCounter = 0
	g.arrayType = -1
	g.arrayBase = -1

def p_array_access_prep(p):
	'array_access_prep : empty'

	g.oStack.pop()
	g.typeStack.pop()

	if g.actualVarObj.dimension_list:
		g.dim = 1
		g.dStack.append((g.actualVarObj.virtual_address, g.dim))
		
		# Push fake bottom
		g.operStack.append(getOperationCode('('))

		g.processingVar = True
	else:
		print('Error: Acceso a variable no dimensionada')


def p_array_access(p):
	'array_access : empty'

	dimension = g.actualVarObj.dimension_list.first
	i = 1
	while i < g.dim:
		dimension = dimension.next
		i += 1

	# All our arrays have 0 as inferior limit
	quad = QuadrupleItem(VERIFY, g.oStack[-1], 0, dimension.sup_lim)
	Quadruple.add_quad(quad)

	# Multidimensional array logic
	if dimension.next:
		aux = g.oStack.pop()
		aux_type = g.typeStack.pop()
		res_address = TempMemory.getAddress(aux_type)
		quad = QuadrupleItem(getOperationCode('*'), aux, dimension, res_address)
		Quadruple.add_quad(quad)
		push_o(res_address, aux_type)

	if g.dim > 1:
		aux_2 = g.oStack.pop()
		aux_2_type = g.typeStack.pop()
		aux_1 = g.oStack.pop()
		aux_1_type = g.typeStack.pop()
		res_address = TempMemory.getAddress(aux_2_type)
		quad = QuadrupleItem(getOperationCode('+'), aux_1, aux_2, res_address)
		Quadruple.add_quad(quad)
		push_o(res_address, aux_1_type)

def p_finish_array_access(p):
	'finish_array_access : empty'

	if g.processingVar:
		aux = g.oStack.pop()
		aux_type = g.typeStack.pop()
		res_address = TempMemory.getAddress(aux_type)

		temp_size = g.actualVarObj.virtual_address
		type = getTypeCode('entero')
		address = TempMemory.getAddress(type)
		TempMemory.setValue(address, temp_size)

		# We don't have to calculate the K constant because all our arrays have an inferior limit of 0
		quad = QuadrupleItem(getOperationCode('+'), aux, address, res_address)
		Quadruple.add_quad(quad)

		push_o('*' + str(res_address), 'entero')
		
		g.operStack.pop()
		g.dStack.pop()

		g.processingVar = False

def p_finish_assignment(p):
	'finish_assignment : empty'

	if(len(g.operStack) > 0):
		if (g.operStack[-1] == getOperationCode('=')):
			left_o = g.oStack.pop()
			res = g.oStack.pop()

			print("%s %s" % (left_o, res))
			operand = g.operStack.pop()

			right_type = g.typeStack.pop()
			left_type = g.typeStack.pop()
			resultType = getResultType(left_type, operand, right_type)

			if resultType > 0:
				quad = QuadrupleItem(operand, left_o, '', res)
				Quadruple.add_quad(quad)
			else:
				print('No puedo asignar ' + str(res) + ' del tipo ' + getTypeStr(right_type) + ' a la variable ' + str(left_o) + ' por que es ' + getTypeStr(left_type))
				sys.exit()	
