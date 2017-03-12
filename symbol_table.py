import sys

class Variable:

	def __init__(self, name, type, value):
		self.name = names
		self.type = type
		self.value = value

class  Function:

	def __init__(self, name, returnType, params, vars):
		self.name = name
		self.returnType = returnType
		self.params = params
		self.vars = {}

	def add_var(self, var):
		'''
			add_var

			Adds a variable to the function scope

			Arguments: var variable object
		'''

		if var.name in self.vars:
			print "Error variable already defined within function scope"

		else:
			self.vars[var.name] = var

class SymbolsTable:
	'''docstring for SymbolsTable'''

	global_scope = Function('global', 'void', None, None)

	main_scope = Function('lienzo', 'void', None, None)

	function_dictionary = {
		'program' : global_scope,
		'lienzo' : main_scope
	}

	__shared_state = {}

	def __init__(self):
		self.__dict__ = sefl.__shared_state

	@classmethod
	def add_function(cls, function):


		if function.name in cls.function_dictionary:
			print "Error function " + function.name + " already defined"

		else:
			cls.function_dictionary[function.name] = function

	@classmethod
	def printFunctionTable(cls):
		for key in cls.function_dictionary:
				print(key)
				print(cls.function_dictionary[key].returnType)
				print(cls.function_dictionary[key].params)
				print('--------------')

	@classmethod
	def add_var_to_func(cls, function, var):
		cls.function_dictionary[function.name].add_var(var)



















