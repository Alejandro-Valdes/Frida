
def init():
	global funcParams
	global funcType
	global funcName
	global funcTypeSoon
	global paramTypeSoon
	global varTypeSoon
	global varName
	global oStack
	global operStack
	global typeStack
	
	oStack = []
	operStack = []
	typeStack = []
	funcParams = []
	funcType = None
	funcName = None
	funcTypeSoon = False
	paramTypeSoon = False
	varTypeSoon = False
	varName = ''