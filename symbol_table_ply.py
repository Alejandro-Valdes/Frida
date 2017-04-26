from symbol_table import *
import global_vars as g
from quadruples import Quadruple
from memory import *
from dimension import *

# Defino variables globales a usar para la tabla de simbolos
# REGLAS PARA TABLA DE SIMBOLOS

def p_check_variable(p):
	'check_variable : empty'
	g.currId = p[-1]
	g.actualVarObj = SymbolsTable.checkVariable(g.currId, g.funcName)

def p_check_function(p):
	'check_function : empty'
	g.funcExpName = p[-1]
	SymbolsTable.checkFunction(p[-1])

def p_saveFuncParam(p):
	'saveFuncParam : empty'
	SymbolsTable.add_function_params(g.funcName, g.funcParams)

def p_saveFuncName(p):
	'saveFuncName : empty'
	g.funcName = p[-1]
	function = Function(g.funcName, g.nextType, None, None, None)
	SymbolsTable.add_function(function)

def p_cleanFunc(p):
	'cleanFunc : empty'
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
	g.funcTypeSoon = True

def  p_saveType(p):
	'saveType : empty'

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
	g.varName = p[-1]

	if g.funcName == 'global':
		virtual_address = GlobalMemory.getAddress(getTypeCode(g.nextType))
	else:
		virtual_address = LocalMemory.getAddress(getTypeCode(g.nextType))

	SymbolsTable.add_var_to_func(g.varName, g.nextType, virtual_address, g.funcName)

def p_paramTypeNext(p):
	'paramTypeNext : empty'
	g.paramTypeSoon = True

def p_printFuncTable(p):
	'printFuncTable : empty'
	SymbolsTable.printFunctionTable()

def p_add_global_scope(p):
	'add_global_scope : empty'

	g.funcName = 'global'
	function = Function(g.funcName, 'void', [], None, None)
	SymbolsTable.add_function(function)

def p_add_main_scope(p):
	'add_main_scope : empty'

	g.funcName = p[-1]
	function = Function(p[-1], 'void', [], None, None)
	SymbolsTable.add_function(function)

	mainPI = len(Quadruple.quadruple_list)
	Quadruple.quadruple_list[0].res = str(mainPI) 

def p_expect_var_type(p):
	'expect_var_type : empty'
	g.varTypeSoon = True

def p_add_func_var_name(p):
	'add_func_var_name : empty'
	g.processingVar = True
	g.varName = g.funcExpName

def p_add_var_name(p):
	'add_var_name : empty'
	g.processingVar = True
	g.varName = p[-1]

def p_add_var(p):
	'add_var : empty'

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

	if g.currentVarDimensions == None:
		g.currentVarDimensions = DimensionList(p[-1])
	else: 
		g.currentVarDimensions.add_dimension(p[-1])

def p_add_quad_count(p):
	'add_quad_count : empty'

	actual_quad_count = len(Quadruple.quadruple_list)
	SymbolsTable.addQuadCountToFunc(g.funcName, actual_quad_count)

