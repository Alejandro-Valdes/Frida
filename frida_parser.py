# Autor: Alejandro Valdes y Evan Juarez
# Archivo que funciona para al analisis sintactico de Frida
# usa la libreria ply
import ply.yacc as yacc

# importar la lista de tokens
from frida_lexer import tokens

from symbol_table_ply import *

# importar modulo para tabla de simbolos
from symbol_table import *

# importar reglas para codigo intermedio
from intermediate_code_ply import *

from module_ply import *

# Defino las reglas del lenguaje MyLittleDuck2017
# se definenen como funcciones p_*
# las reglas se escriben de la forma A : a + b
# ejemplo si la funcion se define como p_A
# no es necesario llamar a esa regla con p_A sino con A

# Programa
def p_programa(p):
	'programa : PROGRAMA ID init_quad add_global_scope vars_opt rutinas lienzo printFuncTable printQuadList'

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
	'''rutinas : RUTINA FuncTypeNext rutina_opt COLON ID saveFuncName LPARENTHESIS parametros RPARENTHESIS saveFuncParam bloque_rutina gen_end_proc cleanFunc rutinas_loop 
		| empty'''

def p_rutina_opt(p):
	'''rutina_opt : primitivo
		| figura
		| VOID saveType'''

def p_rutinas_loop(p):
	'rutinas_loop : rutinas'

# Tipo
def p_tipo(p):
	'tipo : tipo_opt'

def p_tipo_opt(p):
	'''tipo_opt : tipo_opt_prim 
		| tipo_opt_fig'''

# Tipo Prim

def p_tipo_opt_prim(p):
	'tipo_opt_prim : expect_var_type primitivo tipo_opt_prim_loop'

def p_tipo_opt_prim_loop(p):
	'tipo_opt_prim_loop : ID add_var_name tipo_opt_prim_2 add_var tipo_opt_prim_loop_2'

def p_tipo_opt_prim_loop_2(p):
	'''tipo_opt_prim_loop_2 : COMA tipo_opt_prim_loop
		| empty'''

def p_tipo_opt_prim_2(p):
	'''tipo_opt_prim_2 : ini_prim
		| tipo_dimensions add_var tipo_opt_prim_3
		| empty'''

def p_tipo_dimensions(p):
	'''tipo_dimensions : LBRACKET INT add_dimensioned_var RBRACKET 
		| empty'''

def p_tipo_opt_prim_3(p):
	'''tipo_opt_prim_3 : ini_prim_v 
		| empty '''

def p_print_hola(p):
	'print_hola : empty'
	print('hola')

# Tipo fig

def p_tipo_opt_fig(p):
	'tipo_opt_fig : add_var_name figura tipo_opt_fig_loop'

def p_tipo_opt_fig_loop(p):
	'tipo_opt_fig_loop : ID add_var tipo_opt_fig_2 tipo_opt_fig_loop_2'

def p_tipo_opt_fig_loop_2(p):
	'''tipo_opt_fig_loop_2 : COMA tipo_opt_fig_loop
		| empty'''

def p_tipo_opt_fig_2(p):
	'''tipo_opt_fig_2 : ini_fgra
		| LBRACKET INT add_dimensioned_var RBRACKET tipo_opt_fig_3 
		| empty '''

def p_tipo_opt_fig_3(p):
	'''tipo_opt_fig_3 : ini_fgra_v 
		| empty'''

# Inicializacion de valores primitivos

def p_ini_prim(p):
	'ini_prim : ASSIGN push_operation add_var logica'

	address = SymbolsTable.checkVarAddress(g.funcName, p[-2])
	type = SymbolsTable.checkVarType(g.funcName, p[-2])
	push_o(str(address), type)
	assign_helper()

# Inicializacion de arreglos con valores primitivos

def p_ini_prim_v(p):
	'ini_prim_v : ASSIGN push_operation init_array LBRACE cte assign_to_array ini_prim_v_loop RBRACE finish_array_assignment'

def p_ini_prim_v_loop(p):
	'''ini_prim_v_loop : COMA cte assign_to_array ini_prim_v_loop 
		| empty'''

# Inicializacion de figuras

def p_ini_fgra(p):
	'ini_fgra : ASSIGN fgra_nva fgra_fin'

# Inicializacion de arreglos de figuras

def p_ini_fgra_v(p):
	'ini_fgra_v : ASSIGN push_operation LBRACE fgra_nva ini_fgras_v_loop RBRACE'

def p_ini_fgras_v_loop(p):
	'''ini_fgras_v_loop : COMA fgra_nva ini_fgras_v_loop
		| empty'''

def p_fgra_nva(p):
	'''fgra_nva : NUEVO fgra_atr
		| empty'''

def p_fgra_atr(p):
	'''fgra_atr : PINCEL save_fig LPARENTHESIS fgra_atr_end 
		| CUAD save_fig LPARENTHESIS exp push_fig_param COMA fgra_atr_end 
		| CIRC save_fig LPARENTHESIS exp push_fig_param COMA fgra_atr_end
		| RECT save_fig LPARENTHESIS exp push_fig_param COMA exp push_fig_param COMA fgra_atr_end
		| TRIANG save_fig LPARENTHESIS exp push_fig_param COMA exp push_fig_param COMA exp push_fig_param COMA exp push_fig_param COMA fgra_atr_end'''

def p_fgra_atr_end(p):
	'fgra_atr_end : exp push_fig_param COMA exp push_fig_param COMA color push_fig_param RPARENTHESIS'

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
	'''cte : STRING push_string
		| INT push_int
		| DOUBLE push_double
		| TRUE push_bool
		| FALSE push_bool'''

# Push to operands stack for quadruples generation
def p_push_string(p):
	'push_string : empty'
	type = getTypeCode('cadena')
	address = CteMemory.getAddress(type, p[-1][1:-1])
	push_o(str(address), 'cadena')

def p_push_int(p):
	'push_int : empty'
	type = getTypeCode('entero')
	address = CteMemory.getAddress(type, p[-1])
	push_o(str(address), 'entero')

def p_push_double(p):
	'push_double : empty'
	type = getTypeCode('decimal')
	address = CteMemory.getAddress(type, p[-1])
	push_o(str(address), 'decimal')

def p_push_bool(p):
	'push_bool : empty'
	type = getTypeCode('bool')
	address = CteMemory.getAddress(type, p[-1])
	val = True if p[-1] == 'verdadero' else False
	push_o(str(address), 'bool')

# parametros

def p_parametros(p):
	'''parametros : param_list parametros_loop
		| empty'''

def p_parametros_loop(p):
	'''parametros_loop : COMA parametros
		| empty'''

def p_param_list(p):
	'''param_list : paramTypeNext tipo_param COLON ID paramID param_list_loop '''

def p_param_list_loop(p):
	'''param_list_loop : COMA param_list
		| empty'''

def p_tipo_param(p):
	'''tipo_param : primitivo 
		| figura''' 

# lienzo

def p_lienzo(p):
	'lienzo : MAIN add_main_scope bloque_rutina'

# Bloque

def p_bloque(p):
	'bloque : LBRACE bloque_loop RBRACE'

def p_bloque_loop(p):
	'''bloque_loop : estatuto bloque_loop
		| empty'''

# Bloque rutina

def p_bloque_rutina(p):
	'bloque_rutina : add_quad_count LBRACE bloque_rutina_opt bloque_rutina_loop RBRACE'

def p_bloque_rutina_opt(p):
	'''bloque_rutina_opt : vars 
		| empty'''

def p_bloque_rutina_loop(p):
	'''bloque_rutina_loop : estatuto bloque_rutina_loop 
		| empty'''

# ESTATUTO 

def p_estatuto(p):
	'''estatuto : asignacion 
		| condicion 
		| ciclo 
		| impresion 
		| accion 
		| llamada
		| retorno'''

def p_retorno(p):
	'retorno : RETURN logica check_return SEMICOLON'

def p_asignacion(p):
	'asignacion : ID check_variable push_operand asignacion_opt finish_array_access ASSIGN push_operation asignacion_opt_2 finish_single_array_assignment SEMICOLON'
	
	# address = SymbolsTable.checkVarAddress(g.funcName, p[1])
	# if address > 0 and address != None:
	# 	type = SymbolsTable.checkVarType(g.funcName, p[1])
	# 	push_o(str(address), type)
	# else:
	# 	push_o(p[1], 'var')

	# assign_helper()

def p_asignacion_opt(p):
	'''asignacion_opt : LBRACKET array_access_prep logica array_access RBRACKET
		| empty'''

def p_asignacion_opt_2(p):
	'''asignacion_opt_2 : logica 
		| lectura
		| fgra_nva '''

# CONDICION

def p_condicion(p):
	'condicion : IF cond_floor condicion_loop condicion_opt if_2'

def p_condicion_loop(p):
	'condicion_loop : LPARENTHESIS logica RPARENTHESIS if_1 bloque condicion_loop_opt'

def p_condicion_loop_opt(p):
	'''condicion_loop_opt : ELIF if_else_3 condicion_loop
		| empty'''

def p_condicion_opt(p):
	'''condicion_opt : ELSE if_else_3 bloque 
		| empty'''
	
# CICLO

def p_ciclo(p):
	'ciclo : WHILE while_1 LPARENTHESIS logica RPARENTHESIS while_2 bloque while_3'

# IMPRESION
def p_impresion(p):
	'impresion : PRINT LPARENTHESIS logica RPARENTHESIS SEMICOLON'
	print_helper()

# LECTURA
def p_lectura(p):
	'lectura : READ LPARENTHESIS RPARENTHESIS'
	g.nextType = SymbolsTable.checkVarType(g.funcName, p[-5])
	read_helper()

# LLAMADA

def p_llamada(p):
	'llamada : ID check_function LPARENTHESIS mod_call_2 llamada_param RPARENTHESIS mod_call_5 SEMICOLON mod_call_6'

def p_llamada_param(p):
	'''llamada_param : logica mod_call_3 llamada_loop
		| empty mod_call_empty'''

def p_llamada_loop(p):
	'''llamada_loop : COMA mod_call_4 llamada_param
		| empty'''

# logica
def p_logica(p):
	'logica : expresion logica_loop'

def p_logica_loop(p):
	'''logica_loop : AND push_operation logica
		| OR push_operation logica
		| empty'''

# expresion

def p_expresion(p):
	'expresion : exp expresion_opt logica_helper'


def p_expresion_opt(p):
	'''expresion_opt : empty
		| GTHAN push_operation exp expresion_helper
		| GETHAN push_operation exp expresion_helper
		| EQUAL push_operation exp expresion_helper
		| NOTEQUAL push_operation exp expresion_helper
		| LTHAN push_operation exp expresion_helper
		| LETHAN push_operation exp expresion_helper'''

# EXP

def p_exp(p):
	'exp : termino exp_loop'

def p_exp_loop(p):
	'''exp_loop : PLUS push_operation exp exp_loop
		| MINUS push_operation exp exp_loop
		| empty'''

# Termino
def p_termino(p):
	'termino : factor termino_loop exp_helper'

def p_termino_loop(p):
	'''termino_loop : TIMES push_operation termino termino_loop
		| DIVIDE push_operation termino termino_loop
		| empty'''

# Factor

def p_factor(p):
	'''factor : LPARENTHESIS push_fake_bottom expresion RPARENTHESIS pop_fake_bottom factor_helper
		| factor_opt factor_opt_2 factor_helper'''

def p_factor_opt(p):
	'''factor_opt : PLUS
		| MINUS
		| empty'''

def p_factor_opt_2(p):
	'''factor_opt_2 : cte
		| id_factor'''

def p_id_factor(p):
	'''id_factor : ID check_variable push_operand id_factor_opt finish_array_access
		| llamadaExp'''

def p_id_factor_opt(p):
	'''id_factor_opt : LBRACKET array_access_prep logica array_access RBRACKET 
		| empty'''

# llamadaExp

def p_llamadaExp(p):
	'llamadaExp : ID check_function LPARENTHESIS mod_call_2 llamada_param RPARENTHESIS mod_call_5 mod_call_6'
	push_o(p[1], 'func')

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
	'''color : CTECOLOR push_string
		| CTEHEXCOLOR push_string'''

# Error rule se tiene que agregar
# Nos indica el error y el numero de linea donde esta
# gracias al contador del lexer
def p_error(p):
	if(p):
		print("Error: sintaxis '" + str(p.value) + "' en linea: " + str(p.lineno))
	else:
		print("Error: sintaxis al final del archivo")
	sys.exit()

# Crea el parser dandole el estado inicial
parser = yacc.yacc(start='programa')
