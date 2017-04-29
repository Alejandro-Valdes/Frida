from frida_parser import parser
import global_vars
import sys

global_vars.init()

def main(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)


if __name__ == '__main__':
	file = "test/" + sys.argv[1]
	main(file)