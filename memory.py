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
	def getItemValue(cls, key):
		return cls.globalMem[key]		

	@classmethod
	def setItem(cls, value, type):
		address = 0
		if type == BOOL:
			if cls.boolCount < LIM:
				cls.globalMem[GLOBALBOOL + cls.boolCount] = value
				address = GLOBALBOOL + cls.boolCount
				cls.boolCount += 1
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				cls.globalMem[ENTERO + cls.enteroCount] = value
				address = GLOBALENTERO + cls.enteroCount
				cls.enteroCount += 1
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				cls.globalMem[DECIMAL + cls.decimalCount] = value
				address = GLOBALDECIMAL + cls.decimalCount
				cls.decimalCount += 1
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				cls.globalMem[CADENA + cls.cadenaCount] = value
				address = GLOBALCADENA + cls.cadenaCount
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
	def getItemValue(cls, key):
		return cls.localMem[key]		

	@classmethod
	def setItem(cls, value, type):
		address = 0
		if type == BOOL:
			if cls.boolCount < LIM:
				cls.localMem[LOCALBOOL + cls.boolCount] = value
				address = LOCALBOOL + cls.boolCount
				cls.boolCount += 1
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if cls.enteroCount < LIM:
				cls.localMem[ENTERO + cls.enteroCount] = value
				address = LOCALENTERO + cls.enteroCount
				cls.enteroCount += 1
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if cls.decimalCount < LIM:
				cls.localMem[DECIMAL + cls.decimalCount] = value
				address = LOCALDECIMAL + cls.decimalCount
				cls.decimalCount += 1
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if cls.cadenaCount < LIM:
				cls.localMem[CADENA + cls.cadenaCount] = value
				address = LOCALCADENA + cls.cadenaCount
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

class ConstMemory():
	
	def __init__(self):
		self.globalMem = {}

		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0

	def getItem(self, key):
		return constMem[key]

	def setItem(self, key, value, type):
		if type == BOOL:
			if self.boolCount < LIM:
				self.boolCount += 1
				self.constMem[key] = value
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if self.enteroCount < LIM:
				self.enteroCount += 1
				self.constMem[key] = value
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if self.decimalCount < LIM:
				self.decimalCount += 1
				self.constMem[key] = value
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if self.cadenaCount < LIM:
				self.cadenaCount += 1
				self.constMem[key] = value
			else:
				printMemoryOverflow()

	def clearCount(self):
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0

class TempMemory():
	
	def __init__(self):
		self.globalMem = {}

		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0

	def getItem(self, key):
		return tempMem[key]

	def setItem(self, key, value, type):
		if type == BOOL:
			if self.boolCount < LIM:
				self.boolCount += 1
				self.tempMem[key] = value
			else:
				printMemoryOverflow()
		elif type == ENTERO:
			if self.enteroCount < LIM:
				self.enteroCount += 1
				self.tempMem[key] = value
			else:
				printMemoryOverflow()
		elif type == DECIMAL:
			if self.decimalCount < LIM:
				self.decimalCount += 1
				self.tempMem[key] = value
			else:
				printMemoryOverflow()
		elif type == CADENA:
			if self.cadenaCount < LIM:
				self.cadenaCount += 1
				self.tempMem[key] = value
			else:
				printMemoryOverflow()

	def clearCount(self):
		self.boolCount = 0
		self.enteroCount = 0
		self.decimalCount = 0
		self.cadenaCount = 0