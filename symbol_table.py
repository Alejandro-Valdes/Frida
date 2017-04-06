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
			print("Error: variable " + var.name + " ya se definio dentro del alcance de la funcion")
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
			print("Error: funcion " + function.name + " ya se definio")
			sys.exit()
		else:
			cls.function_dictionary[function.name] = function

	@classmethod
	def params_size(cls, name):
		return len(cls.function_dictionary[name].params)

	@classmethod
	def check_param(cls, name, index):
		if (cls.function_dictionary[name].params) >= 0:
			return cls.function_dictionary[name].params[index]

	@classmethod
	def printFunctionTable(cls):
		print('\n')
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
			print("Error: alcance " + scope + " no definido")
			sys.exit()

	@classmethod
	def add_function_params(cls, scope, params):
		if scope in cls.function_dictionary:
			cls.function_dictionary[scope].params = params
		else:
			print("Error: alcance " + scope + " no definido")
			sys.exit()

	@classmethod
	def checkVariable(cls, var, func):
		if(var in cls.function_dictionary[func].vars):
			pass
		elif(var in cls.function_dictionary['global'].vars):
			pass
		else:
			print('Error: ' + var + ' no esta definida dentro del alcance de la funcion ni como varible global')
			sys.exit()

	@classmethod
	def checkFunction(cls, func):
		if(func not in cls.function_dictionary):
			print('Error: funcion ' + func + ' no esta definida')
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

	@classmethod
	def getFuncPI(cls, func):
		if cls.function_dictionary[func]:
			return cls.function_dictionary[func].quad_cont
		else:
			returnType -1

















