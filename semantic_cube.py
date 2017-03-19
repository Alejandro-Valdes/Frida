
VOID = 0
BOOL = 1
BOOLARRAY = 11
ENTERO = 2
ENTEROARRAY = 22
DECIMAL = 3
DECIMALARRAY = 33
CADENA = 4
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
cubeDict['bool&&bool'] = BOOL

# Or
cubeDict['bool||bool'] = BOOL

def test(p):
	pass
