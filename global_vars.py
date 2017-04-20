
def init():
	global funcParams
	global nextType
	global funcType
	global funcName
	global funcTypeSoon
	global paramTypeSoon
	global varTypeSoon
	global varName
	global oStack
	global operStack
	global typeStack
	global jumpStack
	global figParams
	global param_count
	global funcHasReturn
	global currentVarDimensions
	global processingVar
	global arrayAssignmentCounter
	global arrayBase
	global arrayType
	global dStack
	global actualVarObj
	global dim
	
	oStack = []
	dStack = []
	operStack = []
	jumpStack = []
	typeStack = []
	funcParams = []
	figParams = []
	funcType = None
	nextType = None
	funcName = None
	funcTypeSoon = False
	paramTypeSoon = False
	varTypeSoon = False
	varName = ''
	funcHasReturn = False
	currentVarDimensions = None
	processingVar = False
	arrayAssignmentCounter = 0
	arrayBase = -1
	arrayType = -1
	actualVarObj = None
	dim = 0
