import sys

class Variable:

	def __init__(self, name, type, value, scope):
		self.name = name
		self.type = type
		self.value = value

class Function:

	def __init__(self, name, returnType, params, vars, quad_cont):
		self.name = name
		self.returnType = returnType
		self.params = params
		self.vars = {}
		self.quad_cont = quad_cont

	def add_var(self, var):
		'''
			add_var

			Adds a variable to the function scope

			Arguments: var variable object
		'''

		if var.name in self.vars:
			print("Error variable " + var.name + " already defined within function scope")
			sys.exit()

		else:
			self.vars[var.name] = var

class SymbolsTable:
	'''docstring for SymbolsTable'''

	main_scope = Function('lienzo', 'void', None, None, None)

	function_dictionary = {}

	__shared_state = {}

	def __init__(self):
		self.__dict__ = sefl.__shared_state

	@classmethod
	def add_function(cls, function):

		if function.name in cls.function_dictionary:
			print("Error function " + function.name + " already defined")
			sys.exit()
		else:
			cls.function_dictionary[function.name] = function

	@classmethod
	def printFunctionTable(cls):
		function_dir = cls.function_dictionary
		for key in function_dir:
				print('name: ' + key)
				print('return type: ' + function_dir[key].returnType)
				print('quad count: ' + str(function_dir[key].quad_cont))
				print('params : ' + ', '.join(function_dir[key].params))
				print('scoped variables:')
				for var_key in function_dir[key].vars:
					print('\t' + function_dir[key].vars[var_key].name + ' ' +function_dir[key].vars[var_key].type)
				print('\n')

	@classmethod
	def add_var_to_func(cls, name, type, value, scope):
		var = Variable(name, type, None, scope)
		if scope in cls.function_dictionary:
			cls.function_dictionary[scope].add_var(var)
		else:
			print("Error scope " + scope + " not defined")
			sys.exit()

	@classmethod
	def add_function_params(cls, scope, params):
		if scope in cls.function_dictionary:
			cls.function_dictionary[scope].params = params
		else:
			print("Error scope " + scope + " not defined")
			sys.exit()

	@classmethod
	def checkVariable(cls, var, func):
		if(var in cls.function_dictionary[func].vars):
			pass
		elif(var in cls.function_dictionary['global'].vars):
			pass
		else:
			print('Error ' + var + ' is not defined within the function or global scope')
			sys.exit()

	@classmethod
	def checkFunction(cls, func):
		if(func not in cls.function_dictionary):
			print('Error ' + func + ' is not defined as a function')
			sys.exit()

	@classmethod
	def checkVarType(cls, func, var):
		if(var in cls.function_dictionary[func].vars):
			return cls.function_dictionary[func].vars[var].type
		elif(var in cls.function_dictionary['global'].vars):
			return cls.function_dictionary['global'].vars[var].type
		else:
			return -1

	@classmethod
	def checkFuncReturnType(cls, func):
		if(cls.function_dictionary[func]):
			return cls.function_dictionary[func].returnType
		else:
			return -1

	@classmethod
	def addQuadCountToFunc(cls, func, quad_cont):
		if (cls.function_dictionary[func]):
			cls.function_dictionary[func].quad_cont = quad_cont
		else:
			return -1

















