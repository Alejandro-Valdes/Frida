import sys
from semantic_cube import *

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

def printMemoryOverflow():
	print('Error: se acabo la memoria')

def printUndefinedValue():
	print('Error: acceso a variable indefinida')

class Memory():
	"""docstring for Memory"""
	def __init__(self):
		pass

	def getValue(self, address):

		try:
			if address < 1000:
				print('Error Mem ' + str(address))
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
				print('Error Mem ' + str(address))
				print(address >= LOCALPINCEL)
				print(address <= LOCALTRIANGULO)
				return
		except KeyError:
			printUndefinedValue()
			return

	def setValue(self, value, address):
		if address < 1000:
			#print('Error set mem')
			# TODO Set mem fig
			#return
			pass
		elif (address >= 1000 and address < 5000) or (address >= GLOBALPINCEL and address <= GLOBALTRIANGULO):
			GlobalMemory.setValue(address, value)
		elif (address >= 5000 and address < 9000) or (address >= LOCALPINCEL and address <= LOCALTRIANGULO):
			LocalMemory.setValue(address, value)
		elif address >= 9000 and address < 13000:
			TempMemory.setValue(address, value)
		elif address >= 13000 and address < 17000:
			CteMemory.setValue(address, value)
		else:
			print('Error set mem')
			return

class GlobalMemory():

	globalMem = {}
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
		self.__dict__ = self.__shared_state
		

	@classmethod
	def printGlobalMem(cls):
		print(cls.globalMem)

	@classmethod
	def getItemValue(cls, key):
		return(cls.globalMem[key])		

	@classmethod
	def getAddress(cls, type, size = 1):
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
		cls.globalMem[address] = value

	@classmethod
	def clearCount(self):
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0
			
class LocalMemory():

	localMem = {}
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
		self.__dict__ = self.__shared_state
		

	@classmethod
	def printLocalMem(cls):
		print(cls.localMem)

	@classmethod
	def getItemValue(cls, key):
		return(cls.localMem[key])		

	@classmethod
	def getAddress(cls, type, size = 1):
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
		cls.localMem[address] = value

	@classmethod
	def clearCount(self):
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0

class TempMemory():
	
	tempMem = {}
	boolCount = 0
	enteroCount = 0
	decimalCount = 0
	cadenaCount = 0

	__shared_state = {}
	
	def __init__(self):
		self.__dict__ = self.__shared_state
		
	@classmethod
	def printTempMem(cls):
		print(cls.tempMem)

	@classmethod
	def getItemValue(cls, key):
		return(cls.tempMem[key])		

	@classmethod
	def getAddress(cls, type, size = 1):
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
		cls.tempMem[address] = value

	@classmethod
	def clearCount(self):
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0

class CteMemory():
	
	cteMem = {}
	cteMemRev = {}
	boolCount = 0
	enteroCount = 0
	decimalCount = 0
	cadenaCount = 0

	__shared_state = {}
	
	def __init__(self):
		self.__dict__ = self.__shared_state
		
	@classmethod
	def printCteMem(cls):
		print(cls.cteMem)

	@classmethod
	def getItemValue(cls, key):
		return(cls.cteMem[key])	

	@classmethod
	def getAddress(cls, type, value, size = 1):
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
		cls.cteMem[address] = value

	@classmethod
	def clearCount(self):
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0
