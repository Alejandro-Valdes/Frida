from symbol_table import *
import global_vars as g
from quadruples import Quadruple
from memory import *

# Defino variables globales a usar para la tabla de simbolos
# REGLAS PARA TABLA DE SIMBOLOS

def p_check_variable(p):
	'check_variable : empty'
	SymbolsTable.checkVariable(p[-1], g.funcName)

def p_check_function(p):
	'check_function : empty'
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
	print 'impresion'
	LocalMemory.printLocalMem()
	TempMemory.printTempMem()
	GlobalMemory.printGlobalMem()
	CteMemory.printCteMem()
	print '+++++++++++'
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

def p_add_var_name(p):
	'add_var_name : empty'
	g.varTypeSoon = True

def p_add_var(p):
	'add_var : empty'
	g.varName = p[-1]

	if g.funcName == 'global':
		virtual_address = GlobalMemory.getAddress(getTypeCode(g.nextType))
	else:
		virtual_address = LocalMemory.getAddress(getTypeCode(g.nextType))
	
	SymbolsTable.add_var_to_func(g.varName, g.nextType, virtual_address, g.funcName)

def p_add_quad_count(p):
	'add_quad_count : empty'

	actual_quad_count = len(Quadruple.quadruple_list)
	SymbolsTable.addQuadCountToFunc(g.funcName, actual_quad_count)

