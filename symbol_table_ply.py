from symbol_table import *
import global_vars as g
from quadruples import Quadruple
from memory import *
from dimension import *

# Defino variables globales a usar para la tabla de simbolos
# REGLAS PARA TABLA DE SIMBOLOS

def p_check_fig(p):
	'check_fig : empty'

	"""Regla que revisa si se encuentra definida una variable 
	de tipo figura con el id dado por p[-1]
	"""

	g.fig_name = p[-1]
	g.actualVarObj = SymbolsTable.checkVariable(g.fig_name, g.funcName)

def p_check_variable(p):
	'check_variable : empty'

	"""Regla que revisa si se encuentra definida una variable 
	 con el id dado por p[-1]
	"""

	g.currId = p[-1]
	g.actualVarObj = SymbolsTable.checkVariable(g.currId, g.funcName)

def p_check_function(p):
	'check_function : empty'

	"""Regla que revisa si se encuentra definida una variable
	con el id dado por p[-1]
	"""

	g.funcExpName = p[-1]
	g.funcExpNameStack.append(g.funcExpName)
	print(g.funcExpName)
	SymbolsTable.checkFunction(p[-1])

def p_saveFuncParam(p):
	'saveFuncParam : empty'
	
	"""Regla que guarda los parámetros de la función actual"""

	SymbolsTable.add_function_params(g.funcName, g.funcParams)

def p_saveFuncName(p):
	'saveFuncName : empty'

	"""Regla que crea una función con el id p[-1] y la añade 
	a la tabla de símbolos"""

	g.funcName = p[-1]
	function = Function(g.funcName, g.nextType, None, None, None)
	SymbolsTable.add_function(function)

def p_cleanFunc(p):
	'cleanFunc : empty'

	"""Regla auxiliar para la limpieza del scope actual y la 
	impresión de la memoria"""

	LocalMemory.clearCount()
	TempMemory.clearCount()
	print('impresion')
	LocalMemory.printLocalMem()
	TempMemory.printTempMem()
	GlobalMemory.printGlobalMem()
	CteMemory.printCteMem()
	print('+++++++++++')
	g.funcParams = []
	g.funcName = ''
	g.nextType = ''
	g.funcType = ''

def p_FuncTypeNext(p):
	'FuncTypeNext : empty'

	"""Regla auxiliar que levanta una bandera para indicar 
	que se está esperando el tipo de una función"""

	g.funcTypeSoon = True

def  p_saveType(p):
	'saveType : empty'

	"""Regla que guarda el tipo de la función, parámetro o variable"""

	if g.funcTypeSoon:
		g.nextType = p[-1]
		g.funcType = p[-1]
		g.funcTypeSoon = False 
	elif g.paramTypeSoon:
		g.nextType = p[-1]
		g.funcParams.append(p[-1])
		g.paramTypeSoon = False
	elif g.varTypeSoon:
		g.nextType = p[-1]
		g.varTypeSoon = False
	pass

def p_paramID(p):
	'paramID : empty'

	"""Regla que añade una variable con nombre p[-1] como parámetro al scope 
	de la función actual"""

	g.varName = p[-1]

	if g.funcName == 'global':
		virtual_address = GlobalMemory.getAddress(getTypeCode(g.nextType))
	else:
		virtual_address = LocalMemory.getAddress(getTypeCode(g.nextType))

	SymbolsTable.add_var_to_func(g.varName, g.nextType, virtual_address, g.funcName)

def p_paramTypeNext(p):
	'paramTypeNext : empty'

	"""Regla auxiliar que levanta una bandera para indicar 
	que se está esperando el tipo de un parámetro"""

	g.paramTypeSoon = True

def p_printFuncTable(p):
	'printFuncTable : empty'

	"""Regla auxiliar que llama a la impresión de la tabla de 
	símbolos"""

	SymbolsTable.printFunctionTable()

def p_add_global_scope(p):
	'add_global_scope : empty'

	"""Regla que añade scope global a la tabla de símbolos"""

	g.funcName = 'global'
	function = Function(g.funcName, 'void', [], None, None)
	SymbolsTable.add_function(function)

def p_add_main_scope(p):
	'add_main_scope : empty'

	"""Regla que añade main scope a la tabla de símbolos"""

	g.funcName = p[-1]
	function = Function(p[-1], 'void', [], None, None)
	SymbolsTable.add_function(function)

	mainPI = len(Quadruple.quadruple_list)
	goto = g.jumpStack.pop()
	Quadruple.quadruple_list[goto].res = str(mainPI) 

def p_expect_var_type(p):
	'expect_var_type : empty'

	"""Regla auxiliar que levanta una bandera para indicar 
	que se está esperando el tipo de una variable"""

	g.varTypeSoon = True

def p_add_func_var(p):
	'add_func_var : empty'

	"""Regla auxiliar que levanta una bandera para indicar 
	que se está esperando el tipo de un parámetro"""

	g.varName = g.funcName
	print('----------')
	print(g.varName)
	virtual_address = GlobalMemory.getAddress(getTypeCode(SymbolsTable.checkFuncReturnType(g.varName)))
	SymbolsTable.add_var_to_func(g.varName, g.nextType, virtual_address, 'global')


def p_add_var_name(p):
	'add_var_name : empty'

	"""Regla auxiliar que añade el nombre de la variable
	 como variable global"""

	g.processingVar = True
	g.varName = p[-1]

def p_add_var(p):
	'add_var : empty'

	"""Regla que guarda una variable, ya sea normal o 
	dimensionada, en la tabla de símbolos"""

	if g.processingVar:
		if g.currentVarDimensions == None:
			if g.funcName == 'global':
				virtual_address = GlobalMemory.getAddress(getTypeCode(g.nextType))
			else:
				virtual_address = LocalMemory.getAddress(getTypeCode(g.nextType))
			
			SymbolsTable.add_var_to_func(g.varName, g.nextType, virtual_address, g.funcName)
		else:
			g.currentVarDimensions.calculate_constants()
			size = g.currentVarDimensions.total_size

			if g.funcName == 'global':
				virtual_address = GlobalMemory.getAddress(getTypeCode(g.nextType), size)
			else:
				virtual_address = LocalMemory.getAddress(getTypeCode(g.nextType), size)

			SymbolsTable.add_var_to_func(g.varName, g.nextType, virtual_address, g.funcName, g.currentVarDimensions)

			g.currentVarDimensions = None

		g.processingVar = False


def p_add_dimensioned_var(p):
	'add_dimensioned_var : empty'

	"""Regla que añade una lista de dimensiones a variable global con su primera 
	dimensión inicializada en p[-1]"""

	if g.currentVarDimensions == None:
		g.currentVarDimensions = DimensionList(p[-1])
	else: 
		g.currentVarDimensions.add_dimension(p[-1])

def p_add_quad_count(p):
	'add_quad_count : empty'

	"""Regla que añade el número de instrucción a la función actual"""

	actual_quad_count = len(Quadruple.quadruple_list)
	SymbolsTable.addQuadCountToFunc(g.funcName, actual_quad_count)

