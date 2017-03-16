from symbol_table import *

# Defino variables globales a usar para la tabla de simbolos

funcParams = []
funcType = None
funcName = None
funcTypeSoon = False
paramTypeSoon = False

varTypeSoon = False
varName = ''

# REGLAS PARA TABLA DE SIMBOLOS

def p_check_variable(p):
	'check_variable : empty'
	global funcName
	SymbolsTable.checkVariable(p[-1], funcName)

def p_test2(p):
	'test2 : empty'
	print('llamada ' + p[-1])

def p_saveFuncParam(p):
	'saveFuncParam : empty'
	global funcName, funcParams

	SymbolsTable.add_function_params(funcName, funcParams)

def p_saveFuncName(p):
	'saveFuncName : empty'
	global funcName, funcType
	funcName = p[-1]

	function = Function(funcName, funcType, None, None)

	SymbolsTable.add_function(function)

def p_cleanFunc(p):
	'cleanFunc : empty'
	global funcName, funcType, funcParams

	funcParams = []
	funcName = ''
	funcType = ''

def p_saveFuncTypeVoid(p):
	'saveFuncTypeVoid : empty'
	global funcTypeSoon, paramTypeSoon, funcType

	funcType = p[-1]


def p_FuncTypeNext(p):
	'FuncTypeNext : empty'
	global funcTypeSoon
	funcTypeSoon = True

def  p_saveType(p):
	'saveType : empty'
	
	global funcTypeSoon, funcType, paramTypeSoon, funcParams, varTypeSoon

	if funcTypeSoon:
		funcType = p[-1]
		funcTypeSoon = False 
	elif paramTypeSoon:
		funcType = p[-1]
		funcParams.append(p[-1])
		paramTypeSoon = False
	elif varTypeSoon:
		funcType = p[-1]
		varTypeSoon = False
	pass

def p_paramID(p):
	'paramID : empty'
	global funcType, funcName
	varName = p[-1]
	SymbolsTable.add_var_to_func(varName, funcType, None, funcName)


def p_paramTypeNext(p):
	'paramTypeNext : empty'
	global paramTypeSoon
	paramTypeSoon = True

def p_printFuncTable(p):
	'printFuncTable : empty'
	SymbolsTable.printFunctionTable()

def p_add_global_scope(p):
	'add_global_scope : empty'

	global funcName
	funcName = 'global'
	function = Function(funcName, 'void', [], None)
	SymbolsTable.add_function(function)
	
def p_add_main_scope(p):
	'add_main_scope : empty'

	global funcName
	funcName = p[-1]
	function = Function(p[-1], 'void', [], None)
	SymbolsTable.add_function(function)

def p_add_var_name(p):
	'add_var_name : empty'
	global varTypeSoon
	varTypeSoon = True

def p_add_var(p):
	'add_var : empty'
	global varName, funcType, funcName
	varName = p[-1]
	
	SymbolsTable.add_var_to_func(varName, funcType, None, funcName)