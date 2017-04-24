from frida_parser import parser
import global_vars

global_vars.init()

def readFile(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)

readFile("test/even_rec.frida")

print('\n')