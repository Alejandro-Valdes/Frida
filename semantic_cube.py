
VOID = 0
BOOL = 1
BOOLARRAY = 11
INT = 2
INTARRAY = 22
FLOAT = 3
FLOATARRAY = 33
STRING = 4
STRINGARRAY = 44


cubeDict = {}

# Assignments
cubeDict['bool']['=']['bool'] = BOOL
cubeDict['int']['=']['int'] = INT
cubeDict['float']['=']['float'] = FLOAT
cubeDict['string']['=']['string'] = STRING
cubeDict['float']['=']['int'] = FLOAT

# Sums
cubeDict['int']['+']['int'] = INT
cubeDict['float']['+']['int'] = FLOAT
cubeDict['int']['+']['float'] = FLOAT
cubeDict['float']['+']['float'] = FLOAT

# Substraction
cubeDict['int']['-']['int'] = INT
cubeDict['float']['-']['int'] = FLOAT
cubeDict['float']['-']['float'] = FLOAT
cubeDict['int']['-']['float'] = FLOAT

# Multiplication
cubeDict['int']['*']['int'] = INT
cubeDict['int']['*']['float'] = FLOAT
cubeDict['float']['*']['int'] = FLOAT
cubeDict['float']['*']['float'] = FLOAT

# Division
cubeDict['int']['/']['int'] = INT
cubeDict['int']['/']['float'] = FLOAT
cubeDict['float']['/']['int'] = FLOAT
cubeDict['float']['/']['float'] = FLOAT

# Less than
cubeDict['int']['<']['int'] = BOOL
cubeDict['int']['<']['float'] = BOOL
cubeDict['float']['<']['int'] = BOOL
cubeDict['float']['<']['float'] = BOOL

# Less or equal than
cubeDict['int']['<=']['int'] = BOOL
cubeDict['int']['<=']['float'] = BOOL
cubeDict['float']['<=']['int'] = BOOL
cubeDict['float']['<=']['float'] = BOOL

# Equals
cubeDict['int']['==']['int'] = BOOL
cubeDict['int']['==']['float'] = BOOL
cubeDict['float']['==']['int'] = BOOL
cubeDict['float']['==']['float'] = BOOL
cubeDict['bool']['==']['bool'] = BOOL
cubeDict['string']['==']['string'] = BOOL

# Greater than
cubeDict['int']['>']['int'] = BOOL
cubeDict['int']['>']['float'] = BOOL
cubeDict['float']['>']['int'] = BOOL
cubeDict['float']['>']['float'] = BOOL

# Greater or equal than
cubeDict['int']['>=']['int'] = BOOL
cubeDict['int']['>=']['float'] = BOOL
cubeDict['float']['>=']['int'] = BOOL
cubeDict['float']['>=']['float'] = BOOL

# Different
cubeDict['int']['!=']['int'] = BOOL
cubeDict['int']['!=']['float'] = BOOL
cubeDict['float']['!=']['int'] = BOOL
cubeDict['float']['!=']['float'] = BOOL
cubeDict['string']['!=']['string'] = BOOL
cubeDict['bool']['!=']['bool'] = BOOL

# And
cubeDict['bool']['&&']['bool'] = BOOL

# Or
cubeDict['bool']['||']['bool'] = BOOL

