from frida_parser import parser
import global_vars

global_vars.init()

# Pruebas del analizador lexico y gramatico
def readFile(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)

'''print('\nArchivos Falla:\n')

readFile("test_fail_1.txt")
readFile("test_fail_2.txt")
readFile("test_fail_3.txt")'''

#print('\n#####################')

#print('\nArchivos Exito:\n')
readFile("test/function_test.txt")

#print('\n#####################')
#readFile("test_2.txt")
#print('\n#####################')
#readFile("test_3.txt")

print('\n')