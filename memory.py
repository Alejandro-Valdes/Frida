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

LIM = 1000

def printMemoryOverflow():
	print 'Error: se acabo la memoria'

class GlobalMemory():

	globalMem = {}
	boolCount = 0
	enteroCount = 0
	decimalCount = 0
	cadenaCount = 0

	__shared_state = {}
	
	def __init__(self):
		self.__dict__ = self.__shared_state
		

	@classmethod
	def printGlobalMem(cls):
		print cls.globalMem

	@classmethod
	def getItemValue(cls, key):
		return cls.globalMem[key]		

	@classmethod
	def getAddress(cls, type):
		address = 0
		if type == BOOL:
			if cls.boolCount < LIM:
				address = GLOBALBOOL + cls.boolCount
				cls.globalMem[address] = None
				cls.boolCount += 1
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = GLOBALENTERO + cls.enteroCount
				cls.globalMem[address] = None
				cls.enteroCount += 1
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = GLOBALDECIMAL + cls.decimalCount
				cls.globalMem[address] = None
				cls.decimalCount += 1
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = GLOBALCADENA + cls.cadenaCount
				cls.globalMem[address] = None
				cls.cadenaCount += 1
			else:
				printMemoryOverflow()

		return address

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

	__shared_state = {}
	
	def __init__(self):
		self.__dict__ = self.__shared_state
		

	@classmethod
	def printLocalMem(cls):
		print cls.localMem

	@classmethod
	def getItemValue(cls, key):
		return cls.localMem[key]		

	@classmethod
	def getAddress(cls, type):
		address = 0
		if type == BOOL:
			if cls.boolCount < LIM:
				address = LOCALBOOL + cls.boolCount
				cls.localMem[address] = None
				cls.boolCount += 1
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = LOCALENTERO + cls.enteroCount
				cls.localMem[address] = None
				cls.enteroCount += 1
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = LOCALDECIMAL + cls.decimalCount
				cls.localMem[address] = None
				cls.decimalCount += 1
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = LOCALCADENA + cls.cadenaCount
				cls.localMem[address] = None
				cls.cadenaCount += 1
			else:
				printMemoryOverflow()

		return address

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
		print cls.tempMem

	@classmethod
	def getItemValue(cls, key):
		return cls.tempMem[key]		

	@classmethod
	def getAddress(cls, type):
		address = 0
		if type == BOOL:
			if cls.boolCount < LIM:
				address = TEMPBOOL + cls.boolCount
				cls.tempMem[address] = None
				cls.boolCount += 1
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = TEMPENTERO + cls.enteroCount
				cls.tempMem[address] = None
				cls.enteroCount += 1
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = TEMPDECIMAL + cls.decimalCount
				cls.tempMem[address] = None
				cls.decimalCount += 1
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = TEMPCADENA + cls.cadenaCount
				cls.tempMem[address] = None
				cls.cadenaCount += 1
			else:
				printMemoryOverflow()

		return address

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
		print cls.cteMem

	@classmethod
	def getItemValue(cls, key):
		return cls.cteMem[key]	

	@classmethod
	def getAddress(cls, type, value):
		address = 0
		if value in cls.cteMemRev:
			return cls.cteMemRev[value]

		if type == BOOL:
			if cls.boolCount < LIM:
				address = CTEBOOL + cls.boolCount
				cls.boolCount += 1
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				address = CTEENTERO + cls.enteroCount
				cls.enteroCount += 1
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				address = CTEDECIMAL + cls.decimalCount
				cls.decimalCount += 1
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				address = CTECADENA + cls.cadenaCount
				cls.cadenaCount += 1
			else:
				printMemoryOverflow()

		cls.cteMem[address] = value
		cls.cteMemRev[value] = address
		return address

	@classmethod
	def setValue(cls, address, value):
		pass

	@classmethod
	def clearCount(self):
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0
