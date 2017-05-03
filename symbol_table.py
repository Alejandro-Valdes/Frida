import sys

class Variable:
	"""Clase Variable

	Contiene todos los atributos que se necesitan para identificar una variable
	dentro de la tabla de símbolos
	"""

	def __init__(self, name, type, virtual_address, scope, dimension_list):
		self.name = name
		self.type = type
		self.virtual_address = virtual_address
		self.dimension_list = dimension_list

class Function:
	"""Clase Function

	Contiene todos los atributos que se necesitan para identificar una función 
	dentro de la tabla de símbolos
	"""

	def __init__(self, name, returnType, params, vars, quad_cont):
		self.name = name
		self.returnType = returnType
		self.params = params
		self.vars = {}
		self.quad_cont = quad_cont

	def add_var(self, var):
		''' Agrega una variable al scope de esta scope

			Arguments: var variable object
		'''

		if var.name in self.vars:
			raise Exception("Error: variable " + var.name + " ya se definio dentro del alcance de la funcion")

		else:
			self.vars[var.name] = var


class SymbolsTable:
	'''Class SymbolsTable
	
	Objeto que contiene diccionario y métodos para manejar variables
	y funciones dentro de un ambiente de compilación y ejecución
	'''

	main_scope = Function('lienzo', 'void', None, None, None)

	function_dictionary = {} # Tabla de símbolos

	__shared_state = {}

	def __init__(self):
		self.__dict__ = sefl.__shared_state

	@classmethod
	def add_function(cls, function):
		"""Agrega un scope a la tabla de símbolos
		
		args: 
			function -- Function object
		"""

		if function.name in cls.function_dictionary:
			raise Exception("Error: funcion " + function.name + " ya se definio")

		else:
			cls.function_dictionary[function.name] = function

	@classmethod
	def params_size(cls, name):
		"""Regresa el número de parámetros que recibe la función name

		args:
			name -- string nombre de función
		"""

		return len(cls.function_dictionary[name].params)

	@classmethod
	def check_param(cls, name, index):
		"""Regresa el parámetro con índice index de la función name

		args: 
			name -- string
			index -- int
		"""

		if name in cls.function_dictionary:
			return cls.function_dictionary[name].params[index]

	@classmethod
	def printFunctionTable(cls):
		"""Función auxiliar para imprimir la tabla de símbolos en consola"""
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
		"""Regresa la memoria de cierto scope 

		args: 
			scope -- string
		"""
		scope = str(scope)
		scoped_mem = []
		function_dir = cls.function_dictionary

		for var_key in function_dir[scope].vars:
			scoped_mem.append(str(function_dir[scope].vars[var_key].virtual_address) + ' ')

		return scoped_mem


	@classmethod
	def add_var_to_func(cls, name, type, virtual_address, scope, dimension_list = None):
		"""Agrega una variable a un scope
		
		args: 
			name -- string : nombre de variable
			type -- int : tipo de variable
			virtual_address -- int : dirección virtual de variable
			scope -- string : nombre de scope
			dimension_list -- DimensionList 
		"""

		var = Variable(name, type, virtual_address, scope, dimension_list)
		if scope in cls.function_dictionary:
			cls.function_dictionary[scope].add_var(var)

			return var
		else:
			raise Exception("Error: alcance " + scope + " no definido")

	@classmethod
	def add_function_params(cls, scope, params):
		"""Agrega parámetros a la función scope
		
		args:
			scope -- string : nombre de función
			params -- list : lista de parámetros
		"""
		if scope in cls.function_dictionary:
			cls.function_dictionary[scope].params = params
		else:
			raise Exception("Error: alcance " + scope + " no definido")

	@classmethod
	def get_function_signature(cls, scope):
		"""Regresa la lista de parámetros de una función

		args: 
			scope -- string : nombre scope
		"""

		scope = str(scope)
		if scope in cls.function_dictionary:
			return cls.function_dictionary[scope].params
		else:
			raise Exception("Error: alcance " + scope + " no definido")

	@classmethod
	def get_function_params_addresses(cls, scope):
		"""Regresa una lista con todas las variables de una función
		que fueron pasadas como parámetros de la misma

		args: 
			scope -- string : nombre scope
		"""
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
		"""Regresa la variable var que se encuentra dentro de la función func
		o en un scope global

		args: 
			var -- string : nombre variable
			func -- string : nombre función
		"""
		if(var in cls.function_dictionary[func].vars):
			return cls.function_dictionary[func].vars[var]
		elif(var in cls.function_dictionary['global'].vars):
			return cls.function_dictionary['global'].vars[var]
		else:
			raise Exception('Error: ' + var + ' no esta definida dentro del alcance de la funcion ni como varible global')

	@classmethod
	def checkFunction(cls, func):
		"""Checa si la función existe en la tabla de símbolos

		args:
			func -- string : nombre función
		"""
		if(func not in cls.function_dictionary):
			raise Exception('Error: funcion ' + func + ' no esta definida')

	@classmethod
	def checkVarType(cls, func, var):
		"""Regresa tipo de variable de var dentro de la función func
		
		args:
			func -- string : nombre función
			var -- string : nombre variable
		"""
		if(var in cls.function_dictionary[func].vars):
			return cls.function_dictionary[func].vars[var].type
		elif(var in cls.function_dictionary['global'].vars):
			return cls.function_dictionary['global'].vars[var].type
		else:
			return -1

	@classmethod
	def checkVarAddress(cls, func, var):
		"""Regresa la dirección virtual de var dentro de la función func
		
		args:
			func -- string : nombre función
			var -- string : nombre variable
		"""
		if(var in cls.function_dictionary[func].vars):
			return cls.function_dictionary[func].vars[var].virtual_address
		elif(var in cls.function_dictionary['global'].vars):
			return cls.function_dictionary['global'].vars[var].virtual_address
		else:
			return -1

	@classmethod
	def checkFuncReturnType(cls, func):
		"""Regresa el tipo de retorno de la función func
		
		args:
			func -- string : nombre función
		"""
		if(cls.function_dictionary[func]):
			return cls.function_dictionary[func].returnType
		else:
			return -1

	@classmethod
	def addQuadCountToFunc(cls, func, quad_cont):
		"""Agrega el número de instrucción en el cual empieza la función func
		
		args:
			func -- string : nombre función
			quad_cont -- int : número instrucción
		"""
		if (cls.function_dictionary[func]):
			cls.function_dictionary[func].quad_cont = quad_cont
		else:
			return -1

	@classmethod
	def getFuncPI(cls, func):
		"""Regresa el número de instrucción en el cual empieza la función func
		
		args:
			func -- string : nombre función
		"""
		if cls.function_dictionary[func]:
			return cls.function_dictionary[func].quad_cont
		else:
			returnType -1
