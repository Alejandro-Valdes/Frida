from symbol_table import *
import global_vars as g

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
	function = Function(g.funcName, g.funcType, None, None)
	SymbolsTable.add_function(function)

def p_cleanFunc(p):
	'cleanFunc : empty'

	g.funcParams = []
	g.funcName = ''
	g.funcType = ''

def p_saveFuncTypeVoid(p):
	'saveFuncTypeVoid : empty'

	g.funcType = p[-1]


def p_FuncTypeNext(p):
	'FuncTypeNext : empty'
	g.funcTypeSoon = True

def  p_saveType(p):
	'saveType : empty'
	
	if g.funcTypeSoon:
		g.funcType = p[-1]
		g.funcTypeSoon = False 
	elif g.paramTypeSoon:
		g.funcType = p[-1]
		g.funcParams.append(p[-1])
		g.paramTypeSoon = False
	elif g.varTypeSoon:
		g.funcType = p[-1]
		g.varTypeSoon = False
	pass

def p_paramID(p):
	'paramID : empty'
	g.varName = p[-1]
	SymbolsTable.add_var_to_func(g.varName, g.funcType, None, g.funcName)

def p_paramTypeNext(p):
	'paramTypeNext : empty'
	g.paramTypeSoon = True

def p_printFuncTable(p):
	'printFuncTable : empty'
	SymbolsTable.printFunctionTable()

def p_add_global_scope(p):
	'add_global_scope : empty'

	g.funcName = 'global'
	function = Function(g.funcName, 'void', [], None)
	SymbolsTable.add_function(function)
	
def p_add_main_scope(p):
	'add_main_scope : empty'

	g.funcName = p[-1]
	function = Function(p[-1], 'void', [], None)
	SymbolsTable.add_function(function)

def p_add_var_name(p):
	'add_var_name : empty'
	g.varTypeSoon = True

def p_add_var(p):
	'add_var : empty'
	g.varName = p[-1]
	
	SymbolsTable.add_var_to_func(g.varName, g.funcType, None, g.funcName)