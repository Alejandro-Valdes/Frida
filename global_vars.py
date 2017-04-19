
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
	
	oStack = []
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