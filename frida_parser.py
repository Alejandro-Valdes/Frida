# Autor: Alejandro Valdes y Evan Juarez
# Archivo que funciona para al analisis sintactico de Frida
# usa la libreria ply
import ply.yacc as yacc

# importar la lista de tokens
from frida_lexer import tokens

from symbol_table_ply import *

# importar modulo para tabla de simbolos
from symbol_table import *

# Defino las reglas del lenguaje MyLittleDuck2017
# se definenen como funcciones p_*
# las reglas se escriben de la forma A : a + b
# ejemplo si la funcion se define como p_A
# no es necesario llamar a esa regla con p_A sino con A

# Programa
def p_programa(p):
	'programa : PROGRAMA ID add_global_scope vars_opt rutinas lienzo printFuncTable'
	#Este mensaje solo se imprime si es valido el archivo
	print('Valid Frida file')

def p_vars_opt(p):
	'''vars_opt : vars 
		| empty'''

def p_empty(p):
    'empty :'
    pass

# Vars

def p_vars(p):
	'vars : VAR tipo SEMICOLON vars_loop'

def p_vars_loop(p):
	'''vars_loop : vars
		| empty
	'''

# Rutinas

def p_rutinas(p):
	'rutinas : RUTINA FuncTypeNext rutina_opt COLON ID saveFuncName LPARENTHESIS parametros RPARENTHESIS saveFuncParam bloque_rutina cleanFunc rutinas_loop'

def p_rutina_opt(p):
	'''rutina_opt : primitivo
		| figura
		| VOID saveFuncTypeVoid'''

def p_rutinas_loop(p):
	'''rutinas_loop : rutinas
		| empty '''

# Tipo

def p_tipo(p):
	'tipo : tipo_opt'

def p_tipo_opt(p):
	'''tipo_opt : tipo_opt_prim 
		| tipo_opt_fig'''

# Tipo Prim

def p_tipo_opt_prim(p):
	'tipo_opt_prim : add_var_name primitivo tipo_opt_prim_loop'

def p_tipo_opt_prim_loop(p):
	'tipo_opt_prim_loop : ID add_var tipo_opt_prim_2 tipo_opt_prim_loop_2'

def p_tipo_opt_prim_loop_2(p):
	'''tipo_opt_prim_loop_2 : COMA tipo_opt_prim_loop
		| empty'''

def p_tipo_opt_prim_2(p):
	'''tipo_opt_prim_2 : ini_prim 
		| LBRACKET logica RBRACKET tipo_opt_prim_3
		| empty'''

def p_tipo_opt_prim_3(p):
	'''tipo_opt_prim_3 : ini_prim_v 
		| empty '''

# Tipo fig

def p_tipo_opt_fig(p):
	'tipo_opt_fig : add_var_name figura ID add_var tipo_opt_fig_2'

def p_tipo_opt_fig_loop(p):
	'''tipo_opt_fig_loop : COMA tipo_opt_fig
		| empty'''

def p_tipo_opt_fig_2(p):
	'''tipo_opt_fig_2 : ini_fgra 
		| LBRACKET logica RBRACKET tipo_opt_fig_3 
		| empty '''

def p_tipo_opt_fig_3(p):
	'''tipo_opt_fig_3 : ini_fgra_v 
		| empty'''

# Inicializacion de valores primitivos

def p_ini_prim(p):
	'ini_prim : ASIGN logica'

# Inicializacion de arreglos con valores primarios

def p_ini_prim_v(p):
	'ini_prim_v : ASIGN LBRACE logica ini_prim_v_loop RBRACE'

def p_ini_prim_v_loop(p):
	'''ini_prim_v_loop : COMA logica ini_prim_v_loop 
		| empty'''

# Inicializacion de figuras

def p_ini_fgra(p):
	'ini_fgra : ASIGN fgra_nva'

# Inicitalizacion de arreglos de figuras

def p_ini_fgra_v(p):
	'''ini_fgra_v : ASIGN LBRACE fgra_nva ini_fgras_v_loop RBRACE
		| empty'''

def p_ini_fgras_v_loop(p):
	'''ini_fgras_v_loop : COMA fgra_nva ini_fgras_v_loop
		| empty'''

def p_fgra_nva(p):
	'''fgra_nva : NUEVO fgra_atr
		| empty'''

def p_fgra_atr(p):
	'''fgra_atr : PINCEL LPARENTHESIS fgra_atr_end 
		| CUAD LPARENTHESIS exp COMA fgra_atr_end 
		| CIRC LPARENTHESIS exp COMA fgra_atr_end
		| RECT LPARENTHESIS exp COMA exp COMA fgra_atr_end
		| TRIANG LPARENTHESIS exp COMA exp COMA exp COMA exp COMA fgra_atr_end'''

def p_fgra_atr_end(p):
	'fgra_atr_end : exp COMA exp COMA color RPARENTHESIS'

# Data types

def p_primitivo(p):
	'''primitivo : TYPEINT saveType
		| TYPEDOUBLE saveType
		| TYPEBOOL saveType
		| TYPESTRING saveType'''

def p_figura(p):
	'''figura : PINCEL saveType
		| CUAD saveType
		| RECT saveType
		| CIRC saveType
		| TRIANG saveType'''

def p_cte(p):
	'''cte : STRING 
		| INT
		| DOUBLE
		| BOOL'''	

# parametros

def p_parametros(p):
	'''parametros : param_list parametros_loop
		| empty'''

def p_parametros_loop(p):
	'''parametros_loop : COMA parametros
		| empty'''

def p_param_list(p):
	'''param_list : paramTypeNext tipo_param COLON ID paramID param_list_loop
		| empty '''

def p_param_list_loop(p):
	'''param_list_loop : COMA param_list
		| empty'''

def p_tipo_param(p):
	'''tipo_param : primitivo 
		| figura''' 


# lienzo

def p_lienzo(p):
	'lienzo : MAIN add_main_scope bloque_lienzo'

# Bloque

def p_bloque(p):
	'bloque : LBRACE bloque_loop RBRACE'

def p_bloque_loop(p):
	'''bloque_loop : estatuto bloque_loop
		| empty'''

# Bloque rutina

def p_bloque_rutina(p):
	'bloque_rutina : LBRACE bloque_rutina_opt bloque_rutina_loop bloque_rutina_opt_2 RBRACE'

def p_bloque_rutina_opt(p):
	'''bloque_rutina_opt : vars 
		| empty'''

def p_bloque_rutina_loop(p):
	'''bloque_rutina_loop : estatuto bloque_rutina_loop 
		| empty'''

def p_bloque_rutina_opt_2(p):
	'''bloque_rutina_opt_2 : RETURN logica SEMICOLON
		| empty'''

# Bloque lienzo

def p_bloque_lienzo(p):
	'bloque_lienzo : LBRACE bloque_lienzo_loop RBRACE'

def p_bloque_lienzo_loop(p):
	'''bloque_lienzo_loop : estatuto_lienzo bloque_lienzo_loop 
		| empty'''

# ESTATUTO 

def p_estatuto(p):
	'''estatuto : asignacion 
		| condicion 
		| ciclo 
		| impresion 
		| lectura 
		| accion 
		| llamada
		| comentario'''

def p_estatuto_lienzo(p):
	'''estatuto_lienzo : vars 
		| asignacion 
		| condicion 
		| ciclo 
		| impresion 
		| lectura 
		| accion 
		| llamada
		| comentario'''

def p_comentario(p):
	'comentario : COMMENT'

def p_asignacion(p):
	'asignacion : ID asignacion_opt ASIGN asignacion_opt_2 SEMICOLON'

def p_asignacion_opt(p):
	'''asignacion_opt : LBRACKET logica RBRACKET
		| LBRACKET RBRACKET
		| empty'''

def p_asignacion_opt_2(p):
	'''asignacion_opt_2 : logica 
		| lectura 
		| fgra_nva '''

# CONDICION

def p_condicion(p):
	'condicion : IF condicion_loop condicion_opt'

def p_condicion_loop(p):
	'condicion_loop : LPARENTHESIS logica RPARENTHESIS bloque condicion_loop_opt'

def p_condicion_loop_opt(p):
	'''condicion_loop_opt : ELIF condicion_loop 
		| empty'''

def p_condicion_opt(p):
	'''condicion_opt : ELSE bloque 
		| empty'''
	
# CICLO

def p_ciclo(p):
	'ciclo : WHILE LPARENTHESIS logica RPARENTHESIS bloque'

# IMPRESION
def p_impresion(p):
	'impresion : PRINT LPARENTHESIS logica RPARENTHESIS SEMICOLON'

# LECTURA
def p_lectura(p):
	'lectura : READ LPARENTHESIS RPARENTHESIS'

# LLAMADA

def p_llamada(p):
	'llamada : ID LPARENTHESIS llamada_param RPARENTHESIS SEMICOLON'

def p_llamada_param(p):
	'''llamada_param : exp llamada_loop
		| empty'''

def p_llamada_loop(p):
	'''llamada_loop : COMA exp llamada_loop 
		| empty'''

# logica

def p_logica(p):
	'logica : expresion logica_loop'

def p_logica_loop(p):
	'''logica_loop : AND logica
		| OR logica
		| empty'''

# expresion

def p_expresion(p):
	'expresion : exp expresion_opt'

def p_expresion_opt(p):
	'''expresion_opt : expresion_opt_opt exp 
		| empty'''

def p_expresion_opt_opt(p):
	'''expresion_opt_opt : GTHAN 
		| GETHAN 
		| ASIGN ASIGN 
		| NOTEQUAL 
		| LTHAN 
		| LETHAN'''

# EXP

def p_exp(p):
	'exp : termino exp_loop'

def p_exp_loop(p):
	'''exp_loop : PLUS exp
		| MINUS exp
		| empty'''

# Termino
def p_termino(p):
	'termino : factor termino_loop'

def p_termino_loop(p):
	'''termino_loop : TIMES termino 
		| DIVIDE termino 
		| empty'''

# Factor

def p_factor(p):
	'''factor : LPARENTHESIS expresion RPARENTHESIS 
		| factor_opt factor_opt_2'''

def p_factor_opt(p):
	'''factor_opt : PLUS 
		| MINUS 
		| empty'''

def p_factor_opt_2(p):
	'''factor_opt_2 : cte 
		| idllamada'''

# idLlamada
def p_idllamada(p):
	'idllamada : ID idllamada_opt'

def p_idllamada_opt(p):
	'''idllamada_opt : LPARENTHESIS exp idllamada_opt_loop RPARENTHESIS 
		| LPARENTHESIS idllamada_opt_loop RPARENTHESIS	
		| LBRACKET expresion RBRACKET 
		| empty'''

def p_idllamada_opt_loop(p):
	'''idllamada_opt_loop : COMA exp idllamada_opt_loop 
		| empty'''

# accion
def p_accion(p):
	'accion : ID POINT accion_opt SEMICOLON'

def p_accion_opt(p):
	'''accion_opt : accion_figura 
		| accion_pincel'''

# accion figura
def p_accion_figura(p):
	'accion_figura : accion_figura_opt RPARENTHESIS'

def p_accion_figura_opt(p):
	'''accion_figura_opt : accion_figura_opt_2 
		| accion_figura_opt_3'''

def p_accion_figura_opt_2(p):
	'''accion_figura_opt_2 : MOVEA accion_figura_opt_2_end 
		| ROTATE accion_figura_opt_2_end 
		| GROW accion_figura_opt_2_end 
		| THICK accion_figura_opt_2_end'''

def p_accion_figura_opt_2_end(p):
	'accion_figura_opt_2_end : LPARENTHESIS expresion '

def p_accion_figura_opt_3(p):
	'''accion_figura_opt_3 : REMOVE LPARENTHESIS 
		| FILL LPARENTHESIS color'''

# Accion pincel

def p_accion_pincel(p):
	'accion_pincel : accion_pincel_opt RPARENTHESIS'

def p_accion_pincel_opt(p):
	'''accion_pincel_opt : COLOR LPARENTHESIS color 
		| DISPLACE accion_pincel_opt_end 
		| PAINT accion_pincel_opt_end 
		| GRAPH LPARENTHESIS CTEFUNCION COMA exp'''

def p_accion_pincel_opt_end(p):
	'accion_pincel_opt_end : LPARENTHESIS expresion COMA expresion'

# Color
def p_color(p):
	'''color : CTECOLOR
		| CTEHEXCOLOR'''

# Error rule se tiene que agregar
# Nos indica el error y el numero de linea donde esta
# gracias al contador del lexer
def p_error(p):
	if(p):
		print("Syntax error '" + str(p.value) + "' in input line: " + str(p.lineno))
	else:
		print("Syntax error at the end of the file")

# Crea el parser dandole el estado inicial
parser = yacc.yacc(start='programa')

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
readFile("test_1.txt")

#print('\n#####################')
#readFile("test_2.txt")
#print('\n#####################')
#readFile("test_3.txt")

print('\n')

