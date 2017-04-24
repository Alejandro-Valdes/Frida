
VOID = 0
BOOL = 1
ENTERO = 2
DECIMAL = 3
CADENA = 4

BOOLARRAY = 11
ENTEROARRAY = 12
DECIMALARRAY = 13
CADENAARRAY = 14

PINCEL = 20
CUADRADO = 21
RECTANGULO = 22
CIRCULO = 23
TRIANGULO = 24

ASSIGN = 50

ANDORSTART = 60
AND = 61
OR = 62
ANDOREND = 63

RELSTART = 50
LTHAN = 51
GTHAN = 52
EQUAL = 53
DIFF = 54
LETHAN = 55
GETHAN = 56
RELEND = 57

MATHSTART = 80
SUM = 81
SUB = 82
MULT = 83
DIV = 84
MATHEND = 85

VAR = 100
FUNC = 101

PRINT = 200
READ = 300

RET = 400

GOTO = 1000
GOTOF = 1001
TRUE = 1002
FALSE = 1003

ENDPROC = 1005
ERA = 1006
RET = 1007
GOSUB = 1008
PARAM = 1009

# Language native functions
FIG = 2000
F_PAR = 2001
F_FIN = 2002

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
cubeDict[(CADENA, SUM, CADENA)] = CADENA

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
	elif strType == 'pincel':
		return PINCEL
	elif strType == 'cuadrado':
		return CUADRADO
	elif strType == 'rectangulo':
		return RECTANGULO
	elif strType == 'circulo':
		return CIRCULO
	elif strType == 'triangulo':
		return TRIANGULO

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
	elif strType == PINCEL:
		return 'pincel'
	elif strType == CUADRADO:
		return 'cuadrado'
	elif strType == RECTANGULO:
		return 'rectangulo'
	elif strType == CIRCULO:
		return 'circulo'
	elif strType == TRIANGULO:
		return 'triangulo'
