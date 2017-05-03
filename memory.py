import sys
from semantic_cube import *

# Constantes de memoria

GLOBALBOOL = 1000
GLOBALENTERO = 2000
GLOBALDECIMAL = 3000
GLOBALCADENA = 4000

LOCALBOOL = 5000
LOCALENTERO = 6000
LOCALDECIMAL = 7000
LOCALCADENA = 8000

TEMPBOOL = 9000
TEMPENTERO = 10000
TEMPDECIMAL = 11000
TEMPCADENA = 12000

CTEBOOL = 13000
CTEENTERO = 14000
CTEDECIMAL = 15000
CTECADENA = 16000

GLOBALPINCEL = 20000
GLOBALCUADRADO = 21000
GLOBALRECTANGULO = 22000
GLOBALCIRCULO = 23000
GLOBALTRIANGULO = 24000

LOCALPINCEL = 30000
LOCALCUADRADO = 31000
LOCALRECTANGULO = 32000
LOCALCIRCULO = 33000
LOCALTRIANGULO = 34000

LIM = 1000

def printMemoryOverflow(self):
	"""Función auxiliar para la impresión de un memory overflow"""
	raise Exception('Error: se acabo la memoria')

def printUndefinedValue(self):
	"""Función auxiliar para la impresión de un error por variable indefinida"""
	raise Exception('Error: acceso a variable indefinida')

class Memory():
	"""Clase Memory
	
	Mantiene las funciones de más alto nivel de la memoria, 
	haciendo uso de diferentes objetos de memoria que guardan las variables.
	Básicamente, funciona como fachada hacia las demás memorias.
	"""
	def __init__(self):
		"""Inicializador default"""
		pass

	def getValue(self, address):
		"""Regresa valor asociado con la dirección enviada como parámetro

		args: 
			address -- dirección a acceder
		"""

		try:
			if address < 1000:
				raise Exception('Error Mem ' + str(address))
				return
			elif address >= 1000 and address < 5000 or (address >= GLOBALPINCEL and address <= GLOBALTRIANGULO):
				return GlobalMemory.getItemValue(address)
			elif (address >= 5000 and address < 9000) or (address >= LOCALPINCEL and address <= LOCALTRIANGULO):
				return LocalMemory.getItemValue(address)
			elif address >= 9000 and address < 13000:
				return TempMemory.getItemValue(address)
			elif address >= 13000 and address < 17000:
				return CteMemory.getItemValue(address)
			else:
				raise Exception('Error Mem ' + str(address))
				raise Exception(address >= LOCALPINCEL)
				raise Exception(address <= LOCALTRIANGULO)
				return
		except KeyError:
			printUndefinedValue()
			return

	def setValue(self, value, address):
		"""Hace set de un valor en la memoria, 
		regresa excepción si no es posible guardarlo

		args: 
			value -- valor a guardar
			address -- dirección de guardado
		"""

		if address < 1000:
			raise Exception('Error set mem')
		elif (address >= 1000 and address < 5000) or (address >= GLOBALPINCEL and address <= GLOBALTRIANGULO):
			GlobalMemory.setValue(address, value)
		elif (address >= 5000 and address < 9000) or (address >= LOCALPINCEL and address <= LOCALTRIANGULO):
			LocalMemory.setValue(address, value)
		elif address >= 9000 and address < 13000:
			TempMemory.setValue(address, value)
		elif address >= 13000 and address < 17000:
			CteMemory.setValue(address, value)
		else:
			raise Exception('Error set mem')
			return

class GlobalMemory():
	"""Clase GlobalMemory

	Mantiene las variables de scope global
	"""

	globalMem = {} # Diccionario de variables (simula memoria)

	# Contadores de memoria para cada tipo de dato
	boolCount = 0
	enteroCount = 0
	decimalCount = 0
	cadenaCount = 0
	pincelCount = 0
	cuadradoCount = 0
	rectanguloCount = 0
	circuloCount = 0
	trianguloCount = 0

	__shared_state = {}
	
	def __init__(self):
		"""Inicializador default"""
		self.__dict__ = self.__shared_state
		

	@classmethod
	def printGlobalMem(cls):
		"""Función auxiliar para la impresión de la memoria en consola"""
		print(cls.globalMem)

	@classmethod
	def getItemValue(cls, key):
		"""Regresa valor asociado a la key enviada como parámetro
		
		args:
			key -- llave a acceder en la memoria
		"""

		return(cls.globalMem[key])		

	@classmethod
	def getAddress(cls, type, size = 1):
		"""Regresa dirección basado en el tipo de variable, y
		aloca espacio basándose en el tamaño dado.

		args: 
			type -- tipo de variable
			size -- tamaño a alocar en memoria
		"""

		address = 0

		if type == BOOL:
			if cls.boolCount < LIM:
				address = GLOBALBOOL + cls.boolCount
				cls.globalMem[address] = None
				cls.boolCount += size
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = GLOBALENTERO + cls.enteroCount
				cls.globalMem[address] = None
				cls.enteroCount += size
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = GLOBALDECIMAL + cls.decimalCount
				cls.globalMem[address] = None
				cls.decimalCount += size
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = GLOBALCADENA + cls.cadenaCount
				cls.globalMem[address] = None
				cls.cadenaCount += size
			else:
				printMemoryOverflow()
		elif type == PINCEL:
			if cls.pincelCount < LIM:
				address = GLOBALPINCEL + cls.pincelCount
				cls.globalMem[address] = None
				cls.pincelCount += size
			else:
				printMemoryOverflow()
		elif type == CUADRADO:
			if cls.cuadradoCount < LIM:
				address = GLOBALCUADRADO + cls.cuadradoCount
				cls.globalMem[address] = None
				cls.cuadradoCount += size
			else:
				printMemoryOverflow()
		elif type == RECTANGULO:
			if cls.rectanguloCount < LIM:
				address = GLOBALRECTANGULO + cls.rectanguloCount
				cls.globalMem[address] = None
				cls.rectanguloCount += size
			else:
				printMemoryOverflow()
		elif type == CIRCULO:
			if cls.circuloCount < LIM:
				address = GLOBALCIRCULO + cls.circuloCount
				cls.globalMem[address] = None
				cls.circuloCount += size
			else:
				printMemoryOverflow()
		elif type == TRIANGULO:
			if cls.trianguloCount < LIM:
				address = GLOBALTRIANGULO + cls.trianguloCount
				cls.globalMem[address] = None
				cls.trianguloCount += size
			else:
				printMemoryOverflow()

		return address

	@classmethod
	def setValue(cls, address, value):
		"""Hace set de un valor en la dirección enviada
		
		args:
			address -- dirección donde será alocada la variable
			value -- valor de la variable
		"""

		cls.globalMem[address] = value

	@classmethod
	def clearCount(self):
		"""Reset de contadores de cada tipo en memoria"""
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0
			
class LocalMemory():
	"""Clase GlobalMemory

	Mantiene las variables de scope local
	"""

	localMem = {} # Diccionario de variables (simula memoria)

	# Contadores de memoria para cada tipo de dato
	boolCount = 0
	enteroCount = 0
	decimalCount = 0
	cadenaCount = 0
	pincelCount = 0
	cuadradoCount = 0
	rectanguloCount = 0
	circuloCount = 0
	trianguloCount = 0

	__shared_state = {}
	
	def __init__(self):
		"""Inicializador default"""
		self.__dict__ = self.__shared_state
		

	@classmethod
	def printLocalMem(cls):
		"""Función auxiliar para la impresión de la memoria en consola"""

		print(cls.localMem)

	@classmethod
	def getItemValue(cls, key):
		"""Regresa valor asociado a la key enviada como parámetro
		
		args:
			key -- llave a acceder en la memoria
		"""

		return(cls.localMem[key])		

	@classmethod
	def getAddress(cls, type, size = 1):
		"""Regresa dirección basado en el tipo de variable, y
		aloca espacio basándose en el tamaño dado.

		args: 
			type -- tipo de variable
			size -- tamaño a alocar en memoria
		"""

		address = 0

		if type == BOOL:
			if cls.boolCount < LIM:
				address = LOCALBOOL + cls.boolCount
				cls.localMem[address] = None
				cls.boolCount += size
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = LOCALENTERO + cls.enteroCount
				cls.localMem[address] = None
				cls.enteroCount += size
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = LOCALDECIMAL + cls.decimalCount
				cls.localMem[address] = None
				cls.decimalCount += size
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = LOCALCADENA + cls.cadenaCount
				cls.localMem[address] = None
				cls.cadenaCount += size
			else:
				printMemoryOverflow()
		elif type == PINCEL:
			if cls.pincelCount < LIM:
				address = LOCALPINCEL + cls.pincelCount
				cls.localMem[address] = None
				cls.pincelCount += size
			else:
				printMemoryOverflow()
		elif type == CUADRADO:
			if cls.cuadradoCount < LIM:
				address = LOCALCUADRADO + cls.cuadradoCount
				cls.localMem[address] = None
				cls.cuadradoCount += size
			else:
				printMemoryOverflow()
		elif type == RECTANGULO:
			if cls.rectanguloCount < LIM:
				address = LOCALRECTANGULO + cls.rectanguloCount
				cls.localMem[address] = None
				cls.rectanguloCount += size
			else:
				printMemoryOverflow()
		elif type == CIRCULO:
			if cls.circuloCount < LIM:
				address = LOCALCIRCULO + cls.circuloCount
				cls.localMem[address] = None
				cls.circuloCount += size
			else:
				printMemoryOverflow()
		elif type == TRIANGULO:
			if cls.trianguloCount < LIM:
				address = LOCALTRIANGULO + cls.trianguloCount
				cls.localMem[address] = None
				cls.trianguloCount += size
			else:
				printMemoryOverflow()

		return address

	@classmethod
	def setValue(cls, address, value):
		"""Hace set de un valor en la dirección enviada
		
		args:
			address -- dirección donde será alocada la variable
			value -- valor de la variable
		"""

		cls.localMem[address] = value

	@classmethod
	def clearCount(self):
		"""Reset de contadores de cada tipo en memoria"""

		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0

class TempMemory():
	"""Clase TempMemory

	Mantiene las variables temporales	
	"""

	tempMem = {} # Diccionario de variables (simula memoria)

	# Contadores de memoria para cada tipo de dato
	boolCount = 0
	enteroCount = 0
	decimalCount = 0
	cadenaCount = 0

	__shared_state = {}
	
	def __init__(self):
		"""Inicializador default"""

		self.__dict__ = self.__shared_state
		
	@classmethod
	def printTempMem(cls):
		"""Función auxiliar para la impresión de la memoria en consola"""

		print(cls.tempMem)

	@classmethod
	def getItemValue(cls, key):
		"""Regresa valor asociado a la key enviada como parámetro
		
		args:
			key -- llave a acceder en la memoria
		"""
		return(cls.tempMem[key])		

	@classmethod
	def getAddress(cls, type, size = 1):
		"""Regresa dirección basado en el tipo de variable, y
		aloca espacio basándose en el tamaño dado.

		args: 
			type -- tipo de variable
			size -- tamaño a alocar en memoria
		"""

		address = 0

		if type == BOOL:
			if cls.boolCount < LIM:
				address = TEMPBOOL + cls.boolCount
				cls.tempMem[address] = None
				cls.boolCount += size
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = TEMPENTERO + cls.enteroCount
				cls.tempMem[address] = None
				cls.enteroCount += size
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = TEMPDECIMAL + cls.decimalCount
				cls.tempMem[address] = None
				cls.decimalCount += size
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = TEMPCADENA + cls.cadenaCount
				cls.tempMem[address] = None
				cls.cadenaCount += size
			else:
				printMemoryOverflow()

		return address

	@classmethod
	def setValue(cls, address, value):
		"""Hace set de un valor en la dirección enviada
		
		args:
			address -- dirección donde será alocada la variable
			value -- valor de la variable
		"""

		cls.tempMem[address] = value

	@classmethod
	def clearCount(self):
		"""Reset de contadores de cada tipo en memoria"""

		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0

class CteMemory():
	"""Clase CteMemory

	Mantiene las variables constantes
	"""
	
	cteMem = {} # Diccionario de variables 
	cteMemRev = {}

	# Contadores de memoria para cada tipo de dato
	boolCount = 0
	enteroCount = 0
	decimalCount = 0
	cadenaCount = 0

	__shared_state = {}
	
	def __init__(self):
		"""Inicializador default"""

		self.__dict__ = self.__shared_state
		
	@classmethod
	def printCteMem(cls):
		"""Función auxiliar para la impresión de la memoria en consola"""

		print(cls.cteMem)

	@classmethod
	def getItemValue(cls, key):
		"""Regresa valor asociado a la key enviada como parámetro
		
		args:
			key -- llave a acceder en la memoria
		"""

		return(cls.cteMem[key])	

	@classmethod
	def getAddress(cls, type, value, size = 1):
		"""Regresa dirección basado en el tipo de variable, y
		aloca espacio basándose en el tamaño dado.

		args: 
			type -- tipo de variable
			size -- tamaño a alocar en memoria
		"""

		address = 0

		if value in cls.cteMemRev:
			return cls.cteMemRev[value]

		if type == BOOL:
			if cls.boolCount < LIM:
				address = CTEBOOL + cls.boolCount
				cls.boolCount += size
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = CTEENTERO + cls.enteroCount
				cls.enteroCount += size
				value = int(value)
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = CTEDECIMAL + cls.decimalCount
				cls.decimalCount += size
				value = float(value)
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = CTECADENA + cls.cadenaCount
				cls.cadenaCount += size
			else:
				printMemoryOverflow()

		cls.cteMem[address] = value
		cls.cteMemRev[value] = address
		return address

	@classmethod
	def setValue(cls, address, value):
		"""Hace set de un valor en la dirección enviada
		
		args:
			address -- dirección donde será alocada la variable
			value -- valor de la variable
		"""

		cls.cteMem[address] = value

	@classmethod
	def clearCount(self):
		"""Reset de contadores de cada tipo en memoria"""
		
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0
