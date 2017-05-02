from frida_parser import parser
from frida_gui import *
import sys

def main(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)

if __name__ == '__main__':
	# file = "test/" + sys.argv[1]

	root = tk.Tk()
	root.title('Frida IDE')

	root.state('zoomed')

	FridaGui(root, parser).pack(side="top", fill="both", expand=True)
	root.mainloop()
	# main(file)
