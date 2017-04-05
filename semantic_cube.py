
VOID = 0
BOOL = 1
ENTERO = 2
DECIMAL = 3
CADENA = 4

BOOLARRAY = 11
ENTEROARRAY = 22
DECIMALARRAY = 33
CADENAARRAY = 44

ASSIGN = 50
AND = 60
OR = 61
LTHAN = 70
GTHAN = 71
EQUAL = 72
DIFF = 73
LETHAN = 74
GETHAN = 75
SUM = 80
SUB = 81
MULT = 90
DIV = 91

VAR = 100
FUNC = 101

PRINT = 200
READ = 300

RET = 400
cubeDict = {}

# Assignments
cubeDict[(BOOL, ASSIGN, BOOL)] = BOOL
cubeDict[(ENTERO, ASSIGN, ENTERO)] = ENTERO
cubeDict[(DECIMAL, ASSIGN, DECIMAL)] = DECIMAL
cubeDict[(CADENA, ASSIGN, CADENA)] = CADENA
cubeDict[(DECIMAL, ASSIGN, ENTERO)] = DECIMAL

# And OR
cubeDict[(BOOL, AND, BOOL)] = BOOL
cubeDict[(BOOL, OR, BOOL)] = BOOL

# Less than
cubeDict[(ENTERO, LTHAN ,ENTERO)] = BOOL
cubeDict[(ENTERO, LTHAN ,DECIMAL)] = BOOL
cubeDict[(DECIMAL, LTHAN ,ENTERO)] = BOOL
cubeDict[(DECIMAL, LTHAN ,DECIMAL)] = BOOL

# Less or equal than
cubeDict[(ENTERO, LETHAN ,ENTERO)] = BOOL
cubeDict[(ENTERO, LETHAN ,DECIMAL)] = BOOL
cubeDict[(DECIMAL, LETHAN ,ENTERO)] = BOOL
cubeDict[(DECIMAL, LETHAN ,DECIMAL)] = BOOL

# Equals
cubeDict[(ENTERO, EQUAL, ENTERO)] = BOOL
cubeDict[(ENTERO, EQUAL, DECIMAL)] = BOOL
cubeDict[(DECIMAL, EQUAL, ENTERO)] = BOOL
cubeDict[(DECIMAL, EQUAL, DECIMAL)] = BOOL
cubeDict[(BOOL, EQUAL, BOOL)] = BOOL
cubeDict[(CADENA, EQUAL, CADENA)] = BOOL

# Greater than
cubeDict[(ENTERO, GTHAN, ENTERO)] = BOOL
cubeDict[(ENTERO, GTHAN, DECIMAL)] = BOOL
cubeDict[(DECIMAL, GTHAN, ENTERO)] = BOOL
cubeDict[(DECIMAL, GTHAN, DECIMAL)] = BOOL

# Greater or equal than
cubeDict[(ENTERO, GETHAN, ENTERO)] = BOOL
cubeDict[(ENTERO, GETHAN, DECIMAL)] = BOOL
cubeDict[(DECIMAL, GETHAN, ENTERO)] = BOOL
cubeDict[(DECIMAL, GETHAN, DECIMAL)] = BOOL

# Different
cubeDict[(ENTERO, DIFF, ENTERO)] = BOOL
cubeDict[(ENTERO, DIFF, DECIMAL)] = BOOL
cubeDict[(DECIMAL, DIFF, ENTERO)] = BOOL
cubeDict[(DECIMAL, DIFF, DECIMAL)] = BOOL
cubeDict[(CADENA, DIFF, CADENA)] = BOOL
cubeDict[(BOOL, DIFF, BOOL)] = BOOL

# Sums
cubeDict[(ENTERO, SUM, ENTERO)] = ENTERO
cubeDict[(DECIMAL, SUM, ENTERO)] = DECIMAL
cubeDict[(ENTERO, SUM, DECIMAL)] = DECIMAL
cubeDict[(DECIMAL, SUM, DECIMAL)] = DECIMAL

# Substraction
cubeDict[(ENTERO, SUB, ENTERO)] = ENTERO
cubeDict[(DECIMAL, SUB, ENTERO)] = DECIMAL
cubeDict[(ENTERO, SUB, DECIMAL)] = DECIMAL
cubeDict[(DECIMAL, SUB, DECIMAL)] = DECIMAL

# Multiplication
cubeDict[(ENTERO, MULT, ENTERO)] = ENTERO
cubeDict[(DECIMAL, MULT, ENTERO)] = DECIMAL
cubeDict[(ENTERO, MULT, DECIMAL)] = DECIMAL
cubeDict[(DECIMAL, MULT, DECIMAL)] = DECIMAL

# Division
cubeDict[(ENTERO, DIV, ENTERO)] = ENTERO
cubeDict[(DECIMAL, DIV, ENTERO)] = DECIMAL
cubeDict[(ENTERO, DIV, DECIMAL)] = DECIMAL
cubeDict[(DECIMAL, DIV, DECIMAL)] = DECIMAL

cubeDict[(ENTERO, RET, ENTERO)] = ENTERO
cubeDict[(DECIMAL, RET, ENTERO)] = DECIMAL
cubeDict[(DECIMAL, RET, DECIMAL)] = DECIMAL
cubeDict[(BOOL, RET, BOOL)] = BOOL
cubeDict[(CADENA, RET, CADENA)] = CADENA

def getResultType(left,operation,right):
	if ((left,operation,right) in cubeDict):
		return cubeDict[left,operation,right];
	else:
		return -1;

def getOperationCode(code):
	if(code == '='):
		return ASSIGN
	elif(code == 'y'):
		return AND
	elif(code == 'o'):
		return OR
	elif(code == '<'):
		return LTHAN
	elif(code == '>'):
		return GTHAN
	elif(code == '=='):
		return EQUAL
	elif(code == '!='):
		return DIFF
	elif(code == '<='):
		return LETHAN
	elif(code == '>='):
		return GETHAN
	elif(code == '+'):
		return SUM
	elif(code == '-'):
		return SUB
	elif(code == '*'):
		return MULT
	elif(code == '/'):
		return DIV
	elif(code == 'print'):
		return PRINT
	elif(code == 'read'):
		return READ
	elif(code == 'return'):
		return RET
	else:
		return -1

def getOperationStr(code):
	if(code == ASSIGN):
		return '=' 
	elif(code == AND):
		return 'y' 
	elif(code == OR):
		return 'o' 
	elif(code == LTHAN):
		return '<' 
	elif(code == GTHAN):
		return '>' 
	elif(code == EQUAL):
		return '==' 
	elif(code == DIFF):
		return '!=' 
	elif(code == LETHAN):
		return '<=' 
	elif(code == GETHAN):
		return '>=' 
	elif(code == SUM):
		return '+' 
	elif(code == SUB):
		return '-' 
	elif(code == MULT):
		return '*' 
	elif(code == DIV):
		return '/' 
	elif(code == PRINT):
		return 'imprimir' 
	elif(code == READ):
		return 'leer' 
	elif(code == RET):
		return 'regresa' 
	else:
		return -1

def getTypeCode(strType):
	if strType == 'void':
		return VOID
	elif strType == 'bool':
		return BOOL
	elif strType == 'entero':
		return ENTERO
	elif strType == 'decimal':
		return DECIMAL
	elif strType == 'cadena':
		return CADENA

def getTypeStr(codeType):
	if codeType ==  VOID:
		return 'void'
	elif codeType ==  BOOL:
		return 'bool'
	elif codeType ==  ENTERO:
		return 'entero'
	elif codeType ==  DECIMAL:
		return 'decimal'
	elif codeType ==  CADENA:
		return 'cadena'
