
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programaASIGN LTHAN GTHAN NOTEQUAL COLON SEMICOLON LBRACE RBRACE LPARENTHESIS RPARENTHESIS POINT COMA PLUS MINUS TIMES DIVIDE INT STRING FLOAT ID TYPEINT TYPEFLOAT ELSE PRINT PROGRAMA VAR IFprograma : PROGRAMA ID COLON programa2programa2 : vars \n    \t| bloquevars : VAR vars2vars2 : ID vars3vars3 : COMA vars2 \n\t\t| COLON tipo SEMICOLON vars2\n\t\t| COLON tipo SEMICOLON \n\t\t| COLON tipo SEMICOLON bloque \n\t\t| vars2 tipo : TYPEINT \n\t\t| TYPEFLOATbloque : LBRACE bloque2bloque2 : estatuto bloque2 \n\t\t| RBRACEestatuto : asignacion \n\t\t| condicion \n\t\t| escrituraasignacion : ID ASIGN expresion SEMICOLONcondicion : IF LPARENTHESIS expresion RPARENTHESIS bloque condicion2condicion2 : SEMICOLON \n\t\t| ELSE bloque SEMICOLONescritura : PRINT LPARENTHESIS escritura2escritura2 : expresion escritura3 escritura3 : POINT escritura2 \n\t\t| RPARENTHESIS SEMICOLONexpresion : exp \n\t\t| exp expresion2expresion2 : GTHAN expresion \n\t\t| LTHAN expresion \n\t\t| NOTEQUAL expresionexp : termino \n\t\t| termino exp2exp2 : PLUS exp \n\t\t| MINUS exptermino : factor \n\t\t| factor termino2termino2 : TIMES termino \n\t\t| DIVIDE terminofactor : LPARENTHESIS expresion RPARENTHESIS \n\t\t| varcte \n\t\t| PLUS varcte \n\t\t| MINUS varctevarcte : ID \n\t\t| INT \n\t\t| FLOAT \n\t\t| STRING'
    
_lr_action_items = {'NOTEQUAL':([30,31,33,34,36,37,38,41,52,53,62,63,69,70,71,75,76,],[-45,-46,-44,-47,-32,56,-36,-41,-42,-33,-37,-43,-40,-34,-35,-39,-38,]),'DIVIDE':([30,31,33,34,38,41,52,63,69,],[-45,-46,-44,-47,60,-41,-42,-43,-40,]),'GTHAN':([30,31,33,34,36,37,38,41,52,53,62,63,69,70,71,75,76,],[-45,-46,-44,-47,-32,58,-36,-41,-42,-33,-37,-43,-40,-34,-35,-39,-38,]),'VAR':([4,],[8,]),'PRINT':([5,12,13,14,18,39,50,65,67,68,80,82,84,],[15,-16,15,-17,-18,-23,-24,-19,-25,-26,-21,-20,-22,]),'MINUS':([22,23,24,30,31,32,33,34,36,38,41,48,52,54,55,56,58,59,60,61,62,63,69,75,76,],[40,40,40,-45,-46,40,-44,-47,55,-36,-41,40,-42,40,40,40,40,40,40,40,-37,-43,-40,-39,-38,]),'STRING':([22,23,24,32,35,40,48,54,55,56,58,59,60,61,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'SEMICOLON':([10,11,21,30,31,33,34,36,37,38,41,43,44,45,46,49,52,53,57,62,63,69,70,71,72,73,74,75,76,77,83,],[-13,-15,-14,-45,-46,-44,-47,-32,-27,-36,-41,65,66,-11,-12,68,-42,-33,-28,-37,-43,-40,-34,-35,-31,-29,-30,-39,-38,80,84,]),'POINT':([29,30,31,33,34,36,37,38,41,52,53,57,62,63,69,70,71,72,73,74,75,76,],[48,-45,-46,-44,-47,-32,-27,-36,-41,-42,-33,-28,-37,-43,-40,-34,-35,-31,-29,-30,-39,-38,]),'TIMES':([30,31,33,34,38,41,52,63,69,],[-45,-46,-44,-47,61,-41,-42,-43,-40,]),'COLON':([3,20,],[4,27,]),'RPARENTHESIS':([29,30,31,33,34,36,37,38,41,42,51,52,53,57,62,63,69,70,71,72,73,74,75,76,],[49,-45,-46,-44,-47,-32,-27,-36,-41,64,69,-42,-33,-28,-37,-43,-40,-34,-35,-31,-29,-30,-39,-38,]),'PLUS':([22,23,24,30,31,32,33,34,36,38,41,48,52,54,55,56,58,59,60,61,62,63,69,75,76,],[35,35,35,-45,-46,35,-44,-47,54,-36,-41,35,-42,35,35,35,35,35,35,35,-37,-43,-40,-39,-38,]),'IF':([5,12,13,14,18,39,50,65,67,68,80,82,84,],[16,-16,16,-17,-18,-23,-24,-19,-25,-26,-21,-20,-22,]),'$end':([1,6,7,9,10,11,19,21,25,26,47,66,78,79,],[0,-2,-1,-3,-13,-15,-4,-14,-5,-10,-6,-8,-7,-9,]),'RBRACE':([5,12,13,14,18,39,50,65,67,68,80,82,84,],[11,-16,11,-17,-18,-23,-24,-19,-25,-26,-21,-20,-22,]),'LPARENTHESIS':([15,16,22,23,24,32,48,54,55,56,58,59,60,61,],[22,23,32,32,32,32,32,32,32,32,32,32,32,32,]),'ASIGN':([17,],[24,]),'LTHAN':([30,31,33,34,36,37,38,41,52,53,62,63,69,70,71,75,76,],[-45,-46,-44,-47,-32,59,-36,-41,-42,-33,-37,-43,-40,-34,-35,-39,-38,]),'TYPEINT':([27,],[45,]),'COMA':([20,],[28,]),'ELSE':([10,11,21,77,],[-13,-15,-14,81,]),'ID':([2,5,8,12,13,14,18,20,22,23,24,28,32,35,39,40,48,50,54,55,56,58,59,60,61,65,66,67,68,80,82,84,],[3,17,20,-16,17,-17,-18,20,33,33,33,20,33,33,-23,33,33,-24,33,33,33,33,33,33,33,-19,20,-25,-26,-21,-20,-22,]),'TYPEFLOAT':([27,],[46,]),'LBRACE':([4,64,66,81,],[5,5,5,5,]),'INT':([22,23,24,32,35,40,48,54,55,56,58,59,60,61,],[30,30,30,30,30,30,30,30,30,30,30,30,30,30,]),'FLOAT':([22,23,24,32,35,40,48,54,55,56,58,59,60,61,],[31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'PROGRAMA':([0,],[2,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'vars':([4,],[6,]),'termino2':([38,],[62,]),'termino':([22,23,24,32,48,54,55,56,58,59,60,61,],[36,36,36,36,36,36,36,36,36,36,75,76,]),'condicion2':([77,],[82,]),'bloque':([4,64,66,81,],[9,77,79,83,]),'varcte':([22,23,24,32,35,40,48,54,55,56,58,59,60,61,],[41,41,41,41,52,63,41,41,41,41,41,41,41,41,]),'tipo':([27,],[44,]),'exp2':([36,],[53,]),'estatuto':([5,13,],[13,13,]),'vars3':([20,],[25,]),'vars2':([8,20,28,66,],[19,26,47,78,]),'condicion':([5,13,],[14,14,]),'factor':([22,23,24,32,48,54,55,56,58,59,60,61,],[38,38,38,38,38,38,38,38,38,38,38,38,]),'expresion2':([37,],[57,]),'programa2':([4,],[7,]),'escritura2':([22,48,],[39,67,]),'escritura3':([29,],[50,]),'expresion':([22,23,24,32,48,56,58,59,],[29,42,43,51,29,72,73,74,]),'bloque2':([5,13,],[10,21,]),'asignacion':([5,13,],[12,12,]),'programa':([0,],[1,]),'exp':([22,23,24,32,48,54,55,56,58,59,],[37,37,37,37,37,70,71,37,37,37,]),'escritura':([5,13,],[18,18,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> PROGRAMA ID COLON programa2','programa',4,'p_programa','ply_parser.py',16),
  ('programa2 -> vars','programa2',1,'p_programa2','ply_parser.py',21),
  ('programa2 -> bloque','programa2',1,'p_programa2','ply_parser.py',22),
  ('vars -> VAR vars2','vars',2,'p_vars','ply_parser.py',25),
  ('vars2 -> ID vars3','vars2',2,'p_vars2','ply_parser.py',28),
  ('vars3 -> COMA vars2','vars3',2,'p_vars3','ply_parser.py',31),
  ('vars3 -> COLON tipo SEMICOLON vars2','vars3',4,'p_vars3','ply_parser.py',32),
  ('vars3 -> COLON tipo SEMICOLON','vars3',3,'p_vars3','ply_parser.py',33),
  ('vars3 -> COLON tipo SEMICOLON bloque','vars3',4,'p_vars3','ply_parser.py',34),
  ('vars3 -> vars2','vars3',1,'p_vars3','ply_parser.py',35),
  ('tipo -> TYPEINT','tipo',1,'p_tipo','ply_parser.py',38),
  ('tipo -> TYPEFLOAT','tipo',1,'p_tipo','ply_parser.py',39),
  ('bloque -> LBRACE bloque2','bloque',2,'p_bloque','ply_parser.py',42),
  ('bloque2 -> estatuto bloque2','bloque2',2,'p_bloque2','ply_parser.py',45),
  ('bloque2 -> RBRACE','bloque2',1,'p_bloque2','ply_parser.py',46),
  ('estatuto -> asignacion','estatuto',1,'p_estatuto','ply_parser.py',49),
  ('estatuto -> condicion','estatuto',1,'p_estatuto','ply_parser.py',50),
  ('estatuto -> escritura','estatuto',1,'p_estatuto','ply_parser.py',51),
  ('asignacion -> ID ASIGN expresion SEMICOLON','asignacion',4,'p_asignacion','ply_parser.py',54),
  ('condicion -> IF LPARENTHESIS expresion RPARENTHESIS bloque condicion2','condicion',6,'p_condicion','ply_parser.py',57),
  ('condicion2 -> SEMICOLON','condicion2',1,'p_condicion2','ply_parser.py',60),
  ('condicion2 -> ELSE bloque SEMICOLON','condicion2',3,'p_condicion2','ply_parser.py',61),
  ('escritura -> PRINT LPARENTHESIS escritura2','escritura',3,'p_escritura','ply_parser.py',64),
  ('escritura2 -> expresion escritura3','escritura2',2,'p_escritura2','ply_parser.py',67),
  ('escritura3 -> POINT escritura2','escritura3',2,'p_escritura3','ply_parser.py',70),
  ('escritura3 -> RPARENTHESIS SEMICOLON','escritura3',2,'p_escritura3','ply_parser.py',71),
  ('expresion -> exp','expresion',1,'p_expresion','ply_parser.py',74),
  ('expresion -> exp expresion2','expresion',2,'p_expresion','ply_parser.py',75),
  ('expresion2 -> GTHAN expresion','expresion2',2,'p_expresion2','ply_parser.py',78),
  ('expresion2 -> LTHAN expresion','expresion2',2,'p_expresion2','ply_parser.py',79),
  ('expresion2 -> NOTEQUAL expresion','expresion2',2,'p_expresion2','ply_parser.py',80),
  ('exp -> termino','exp',1,'p_exp','ply_parser.py',83),
  ('exp -> termino exp2','exp',2,'p_exp','ply_parser.py',84),
  ('exp2 -> PLUS exp','exp2',2,'p_exp2','ply_parser.py',87),
  ('exp2 -> MINUS exp','exp2',2,'p_exp2','ply_parser.py',88),
  ('termino -> factor','termino',1,'p_termino','ply_parser.py',91),
  ('termino -> factor termino2','termino',2,'p_termino','ply_parser.py',92),
  ('termino2 -> TIMES termino','termino2',2,'p_termino2','ply_parser.py',95),
  ('termino2 -> DIVIDE termino','termino2',2,'p_termino2','ply_parser.py',96),
  ('factor -> LPARENTHESIS expresion RPARENTHESIS','factor',3,'p_factor','ply_parser.py',99),
  ('factor -> varcte','factor',1,'p_factor','ply_parser.py',100),
  ('factor -> PLUS varcte','factor',2,'p_factor','ply_parser.py',101),
  ('factor -> MINUS varcte','factor',2,'p_factor','ply_parser.py',102),
  ('varcte -> ID','varcte',1,'p_varcte','ply_parser.py',105),
  ('varcte -> INT','varcte',1,'p_varcte','ply_parser.py',106),
  ('varcte -> FLOAT','varcte',1,'p_varcte','ply_parser.py',107),
  ('varcte -> STRING','varcte',1,'p_varcte','ply_parser.py',108),
]
