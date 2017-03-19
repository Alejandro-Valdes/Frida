from semantic_cube import *
from symbol_table import *
import global_vars as g


def p_push_operation(p):
	'push_operation : empty'
	g.operStack.append(p[-1])

def p_logica_helper(p):
	'logica_helper : empty'

def p_expresion_helper(p):
	'expresion_helper : empty'

def p_exp_helper(p):
	'exp_helper : empty'

def p_termino_helper(p):
	'termino_helper : empty'

def p_factor_helper(p):
	'factor_helper : empty'

def p_push_fake_bottom(p):
	'push_fake_bottom : empty'
	g.operStack.append(p[-1])

def p_pop_fake_bottom(p):
	'pop_fake_bottom : empty'
	g.operStack.pop()

def push_o(p):

	print p