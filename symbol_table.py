import sys

class Variable:

	def __init__(self, name, type, virtual_address, scope, dimension_list):
		self.name = name
		self.type = type
		self.virtual_address = virtual_address
		self.dimension_list = dimension_list

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
			raise Exception("Error: variable " + var.name + " ya se definio dentro del alcance de la funcion")

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
			raise Exception("Error: funcion " + function.name + " ya se definio")

		else:
			cls.function_dictionary[function.name] = function

	@classmethod
	def params_size(cls, name):
		return len(cls.function_dictionary[name].params)

	@classmethod
	def check_param(cls, name, index):
		if name in cls.function_dictionary:
			return cls.function_dictionary[name].params[index]

	@classmethod
	def printFunctionTable(cls):
		print('\n')
		function_dir = cls.function_dictionary
		for key in function_dir:
				print('name: ' + key)
				print('return type: ' + function_dir[key].returnType)
				print('quad count: ' + str(function_dir[key].quad_cont))
				print('params: ' + ', '.join(function_dir[key].params))
				print('scoped variables:')
				for var_key in function_dir[key].vars:
					print('\t' + function_dir[key].vars[var_key].name + ' ' +function_dir[key].vars[var_key].type 
						+ ' ' + str(function_dir[key].vars[var_key].virtual_address) + ' ' + str(function_dir[key].vars[var_key].dimension_list))
				print('\n')

	@classmethod
	def getScopedMemory(cls, scope):
		scope = str(scope)
		scoped_mem = []
		function_dir = cls.function_dictionary

		for var_key in function_dir[scope].vars:
			scoped_mem.append(str(function_dir[scope].vars[var_key].virtual_address) + ' ')

		return scoped_mem


	@classmethod
	def add_var_to_func(cls, name, type, virtual_address, scope, dimension_list = None):
		var = Variable(name, type, virtual_address, scope, dimension_list)
		if scope in cls.function_dictionary:
			cls.function_dictionary[scope].add_var(var)

			return var
		else:
			raise Exception("Error: alcance " + scope + " no definido")

	@classmethod
	def add_function_params(cls, scope, params):
		if scope in cls.function_dictionary:
			cls.function_dictionary[scope].params = params
		else:
			raise Exception("Error: alcance " + scope + " no definido")

	@classmethod
	def get_function_signature(cls, scope):
		scope = str(scope)
		if scope in cls.function_dictionary:
			return cls.function_dictionary[scope].params
		else:
			raise Exception("Error: alcance " + scope + " no definido")

	@classmethod
	def get_function_params_addresses(cls, scope):
		addresses = []
		scope = str(scope)
		index = 0

		if scope in cls.function_dictionary:
			lenParamas = len(cls.function_dictionary[scope].params)

			for var_key in cls.function_dictionary[scope].vars:
				addresses.append(cls.function_dictionary[scope].vars[var_key].virtual_address)
				index += 1
				if index == lenParamas:
					break

			return addresses

		else:
			raise Exception("Error: alcance " + scope + " no definido")

	@classmethod
	def checkVariable(cls, var, func):
		if(var in cls.function_dictionary[func].vars):
			return cls.function_dictionary[func].vars[var]
		elif(var in cls.function_dictionary['global'].vars):
			return cls.function_dictionary['global'].vars[var]
		else:
			raise Exception('Error: ' + var + ' no esta definida dentro del alcance de la funcion ni como varible global')

	@classmethod
	def checkFunction(cls, func):
		if(func not in cls.function_dictionary):
			raise Exception('Error: funcion ' + func + ' no esta definida')

	@classmethod
	def checkVarType(cls, func, var):
		if(var in cls.function_dictionary[func].vars):
			return cls.function_dictionary[func].vars[var].type
		elif(var in cls.function_dictionary['global'].vars):
			return cls.function_dictionary['global'].vars[var].type
		else:
			return -1

	@classmethod
	def checkVarAddress(cls, func, var):
		if(var in cls.function_dictionary[func].vars):
			return cls.function_dictionary[func].vars[var].virtual_address
		elif(var in cls.function_dictionary['global'].vars):
			return cls.function_dictionary['global'].vars[var].virtual_address
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



















