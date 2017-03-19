
VOID = 0
BOOL = 1
ENTERO = 2
DECIMAL = 3
CADENA = 4

ENTEROARRAY = 22
DECIMALARRAY = 33
BOOLARRAY = 11
CADENAARRAY = 44

cubeDict = {}

# Assignments
cubeDict['bool=bool'] = BOOL
cubeDict['entero=entero'] = ENTERO
cubeDict['decimal=decimal'] = DECIMAL
cubeDict['cadena=cadena'] = CADENA
cubeDict['decimal=entero'] = DECIMAL

# Sums
cubeDict['entero+entero'] = ENTERO
cubeDict['decimal+entero'] = DECIMAL
cubeDict['entero+decimal'] = DECIMAL
cubeDict['decimal+decimal'] = DECIMAL

# Substraction
cubeDict['entero-entero'] = ENTERO
cubeDict['decimal-entero'] = DECIMAL
cubeDict['decimal-decimal'] = DECIMAL
cubeDict['entero-decimal'] = DECIMAL

# Multiplication
cubeDict['entero*entero'] = ENTERO
cubeDict['entero*decimal'] = DECIMAL
cubeDict['decimal*entero'] = DECIMAL
cubeDict['decimal*decimal'] = DECIMAL

# Division
cubeDict['entero/entero'] = ENTERO
cubeDict['entero/decimal'] = DECIMAL
cubeDict['decimal/entero'] = DECIMAL
cubeDict['decimal/decimal'] = DECIMAL

# Less than
cubeDict['entero<entero'] = BOOL
cubeDict['entero<decimal'] = BOOL
cubeDict['decimal<entero'] = BOOL
cubeDict['decimal<decimal'] = BOOL

# Less or equal than
cubeDict['entero<=entero'] = BOOL
cubeDict['entero<=decimal'] = BOOL
cubeDict['decimal<=entero'] = BOOL
cubeDict['decimal<=decimal'] = BOOL

# Equals
cubeDict['entero==entero'] = BOOL
cubeDict['entero==decimal'] = BOOL
cubeDict['decimal==entero'] = BOOL
cubeDict['decimal==decimal'] = BOOL
cubeDict['bool==bool'] = BOOL
cubeDict['cadena==cadena'] = BOOL

# Greater than
cubeDict['entero>entero'] = BOOL
cubeDict['entero>decimal'] = BOOL
cubeDict['decimal>entero'] = BOOL
cubeDict['decimal>decimal'] = BOOL

# Greater or equal than
cubeDict['entero>=entero'] = BOOL
cubeDict['entero>=decimal'] = BOOL
cubeDict['decimal>=entero'] = BOOL
cubeDict['decimal>=decimal'] = BOOL

# Different
cubeDict['entero!=entero'] = BOOL
cubeDict['entero!=decimal'] = BOOL
cubeDict['decimal!=entero'] = BOOL
cubeDict['decimal!=decimal'] = BOOL
cubeDict['cadena!=cadena'] = BOOL
cubeDict['bool!=bool'] = BOOL

# And
cubeDict['boolybool'] = BOOL

# Or
cubeDict['boolobool'] = BOOL

def getResultType(query):
	if (query in cubeDict):
		return cubeDict[query];
	else:
		return -1;
