from frida_parser import parser
import global_vars

global_vars.init()

def readFile(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)

readFile("test/test_mem.txt")

print('\n')