'''
gramatica de JPR
'''
from Expresiones.Relacional import Relacional
from TS.Exception import Excepcion
from Reportes import Reportes as Reports
import os

errores = []
listExceptions = []
reservadas = {
    'var': 'RVAR', 'int': 'RINT', 'double': 'RDOUBLE', 'boolean': 'RBOOL', 'char': 'RCHAR', 'string': 'RSTRING',
    'null': 'RNULL',
    'main': 'RMAIN', 'read': 'RREAD', 'print': 'RPRINT', 'continue': 'RCONTINUE', 'return': 'RRETURN', 'new': 'RNEW',
    'func': 'RFUNC',
    'switch': 'RSWITCH', 'case': 'RCASE', 'default': 'RDEFAULT', 'break': 'RBREAK',
    'toLower': 'RTOLOWER', 'toUpper': 'RTOUPPER',
    'while': 'RWHILE', 'for': 'RFOR',
    'if': 'RIF', 'else': 'RELSE',
    'true': 'RTRUE', 'false': 'RFALSE'
}
tokens = [
             'IGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENIGUAL', 'MAYIGUAL', 'IGUALIGUAL',
             'MAS', 'MENOS', 'MASMAS', 'MENOSMENOS', 'POR', 'DIV', 'MOD', 'POT',
             'PTCOMA', 'DOSPUNTOS', 'COMA', 'COMILLASIMPLE', 'COMILLADOBLE',
             'DECIMAL', 'ENTERO', 'CADENA', 'BOOL', 'CHAR', 'ID',
             'PARA', 'PARC', 'CORA', 'CORC', 'LLAVEA', 'LLAVEC',
             'COMENTARIO', 'COMENTARIOMULTI',
             'OR', 'AND', 'NOT'
         ] + list(reservadas.values())

# set value of TOKENS
t_IGUAL = r'='
t_DIFERENTE = r'=\!'
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENIGUAL = r'<='
t_MAYIGUAL = r'>='
t_IGUALIGUAL = r'=='
t_MAS = r'\+'
t_MENOS = r'-'
t_MASMAS = r'\+\+'
t_MENOSMENOS = r'--'
t_POR = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_POT = r'\*\*'
t_PTCOMA = r';'
t_DOSPUNTOS = r':'
t_COMA = r','
t_COMILLASIMPLE = r'\''
t_COMILLADOBLE = r'\"'
t_PARA = r'\('
t_PARC = r'\)'
t_CORA = r'\['
t_CORC = r'\]'
t_LLAVEA = r'\{'
t_LLAVEC = r'\}'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'\!'


# Comentario de múltiples líneas #* .. *#
def t_COMENTARIOMULTI(t):
    r'\#\*(.|\n)*?\*\#'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple // ...
def t_COMENTARIO(t):
    r'\#.*\n?'
    t.lexer.lineno += 1


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t


def t_CADENA(t):
    r'\"((\\\")|.|\n)*?\"'
    t.value = t.value[1:-1]  # remuevo las comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\"', '\"')
    return t


def t_CHAR(t):
    r'(\'(\\(n|t|\\|\"|\')|.)\')'
    t.value = t.value[1:-1]  # remuevo las comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\"', '\"')
    return t


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    errores.append(Excepcion("Lexico", "Error léxico." + t.value[0], t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Construyendo el analizador léxico
import ply.lex as lex

lexer = lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'MENOR', 'MAYOR', 'IGUALIGUAL', 'MENIGUAL', 'MAYIGUAL', 'DIFERENTE'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'DIV', 'POR', 'MOD'),
    ('left', 'POT'),
    ('right', 'UMENOS'),
)

# Definición de la gramática

# Abstract
from Instrucciones.DeclaraccionArr2 import DeclaracionArr2
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from Instrucciones.ModificarArr import ModificarArr
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Incremento import Incremento
from Instrucciones.Decremento import Decremento
from Instrucciones.Asignacion import Asignacion
from Instrucciones.Continue import Continue
from Instrucciones.Imprimir import Imprimir
from Instrucciones.Llamada import Llamada
from Instrucciones.Funcion import Funcion
from Instrucciones.Return import Return
from Instrucciones.Switch import Switch
from Instrucciones.While import While
from Instrucciones.Break import Break
from Instrucciones.Main import Main
from Instrucciones.Case import Case
from Instrucciones.For import For
from Instrucciones.If import If
from Expresiones.Identificador import Identificador
from Expresiones.AccesoArr import AccesoArr
from Expresiones.Primitivos import Primitivos
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Logica import Logica
from Expresiones.Casteo import Casteo
from Expresiones.Read import Read
from TS.Tipo import OperadorAritmetico, OperadorLogico, OperadorRelacional, TIPO


def p_init(t):
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t):
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
# ///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////
def p_instrucciones_instruccion(t):
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]
# ///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////
def p_instruccion(t):
    '''instruccion      : print
                        | decla
                        | asig
                        | incremento
                        | decremento
                        | sentIf
                        | sentWhile
                        | sentBreak
                        | sentFor
                        | sentSwitch
                        | main
                        | func
                        | llam fin
                        | return fin
                        | continue
                        | declaArr fin
                        | modArr fin'''
    t[0] = t[1]
def p_instruccion_error(t):
    'instruccion        : error PTCOMA'
    errores.append(
        Excepcion("Sintáctico", "Error Sintáctico." + str(t[1].value), t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""

# ///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////
def p_imprimir(t):
    'print     : RPRINT PARA expresion PARC fin'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))
# --------- DECLA AND ASIG
def p_declaracion1(t):
    'decla : RVAR ID fin'
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]))
def p_declaracion2(t):
    'decla : RVAR ID IGUAL expresion fin'
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]), t[4])
def p_asignacion(t):
    'asig : ID IGUAL expresion fin'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
# ------------(++) and (--)
def p_incremento(t):
    'incremento : ID MASMAS fin'
    t[0] = Incremento(t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_decremento(t):
    'decremento : ID MENOSMENOS fin'
    t[0] = Decremento(t[1], t.lineno(1), find_column(input, t.slice[1]))
# --------------- IF
def p_if1(t):
    'sentIf : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))
def p_if2(t):
    'sentIf : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))
def p_if3(t):
    'sentIf : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE sentIf'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))
# ------------------ WHILE
def p_while(t):
    'sentWhile     : RWHILE PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))
# ------------------ BREAK
def p_break(t):
    'sentBreak     : RBREAK fin'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))
# ------------------ CONTINUE
def p_continue(t):
    'continue     : RCONTINUE fin'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))
# ----------------- FOR
def p_for(t):
    '''
    sentFor : RFOR PARA initFor PTCOMA expresion PTCOMA actualizacion PARC LLAVEA instrucciones LLAVEC
    '''
    t[0] = For(t[3],t[5],t[7],t[10],t.lineno(2), find_column(input, t.slice[2]))
# ------------------------------ DECLARACION Y ASIGNACION
def p_init_declaracion(t):
    'initFor : RVAR ID IGUAL expresion'
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]), t[4])
def p_init_asignacion(t):
    'initFor : ID IGUAL expresion'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
def p_actualizacion_asig(t):
    'actualizacion : ID IGUAL expresion'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
def p_actualizacion_incremento(t):
    'actualizacion : ID MASMAS'
    t[0] = Incremento(t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_actualizacion_decremento(t):
    'actualizacion : ID MENOSMENOS'
    t[0] = Decremento(t[1], t.lineno(1), find_column(input, t.slice[1]))
# ------------------------------ DECLARACION ARREGLOS
def p_declArr(t):
    '''declaArr : tipoArr'''
    t[0] = t[1]
def p_tipo1(t):
    '''tipoArr : tipo lista_Dim ID IGUAL RNEW tipo lista_expresiones'''
    t[0] = DeclaracionArr1(t[1], t[2], t[3], t[6], t[7], t.lineno(3), find_column(input, t.slice[3]))
def p_tipo2(t):
    'tipoArr : tipo lista_Dim ID IGUAL ALL_VAL_ARR'
    t[0] = DeclaracionArr2(t[1], t[2], t[3], t[5], t.lineno(3), find_column(input, t.slice[3]))

def p_lista_Dim1(t):
    'lista_Dim     : lista_Dim CORA CORC'
    t[0] = t[1] + 1
def p_lista_Dim2(t):
    'lista_Dim    : CORA CORC'
    t[0] = 1
def p_lista_expresiones_1(t):
    'lista_expresiones     : lista_expresiones CORA expresion CORC'
    t[1].append(t[3])
    t[0] = t[1]
def p_lista_expresiones_2(t):
    'lista_expresiones    : CORA expresion CORC'
    t[0] = [t[2]]
#
def p_valores_arreglo(t):
    'ALL_VAL_ARR : LLAVEA LIST_VAL_ARR LLAVEC'
    t[0]=t[2]

def p_lista_valores_arreglo(t):
    '''LIST_VAL_ARR : LIST_VAL_ARR COMA VAL_ARR'''
    t[1].append(t[3])
    t[0]=t[1]

def p_lista_valores_arreglo2(t):
    '''LIST_VAL_ARR : VAL_ARR'''
    t[0]=[t[1]]

def p_valores_arr(t):
    '''VAL_ARR : ALL_VAL_ARR
                | expresion'''
    t[0]=t[1]
# ------------------------------ MODIFICACION ARREGLOS
def p_modArr(t) :
    '''modArr     :  ID lista_expresiones IGUAL expresion'''
    t[0] = ModificarArr(t[1], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))
# ---------------------------- SWITCH
def p_switch_cases_default(t):
    'sentSwitch : RSWITCH PARA expresion PARC LLAVEA cases default LLAVEC'
    t[0] = Switch(t[3],t[6],t[7],t.lineno(1), find_column(input, t.slice[1]))
def p_switch_cases(t):
    'sentSwitch : RSWITCH PARA expresion PARC LLAVEA cases LLAVEC'
    t[0] = Switch(t[3],t[6],None,t.lineno(1), find_column(input, t.slice[1]))
def p_switch_default(t):
    'sentSwitch : RSWITCH PARA expresion PARC LLAVEA default LLAVEC'
    t[0] = Switch(t[3],None,t[6],t.lineno(1), find_column(input, t.slice[1]))
def p_cases_cases_case(t):
    'cases : cases case'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
def p_cases_case(t):
    'cases    : case'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]
def p_case(t):
    'case : RCASE expresion DOSPUNTOS instrucciones'
    t[0] = Case(t[2],t[4],t.lineno(1), find_column(input, t.slice[1]))
def p_default(t):
    'default : RDEFAULT DOSPUNTOS instrucciones'
    t[0] = t[3]
def p_main(t) :
    'main     : RMAIN PARA PARC LLAVEA instrucciones LLAVEC'
    t[0] = Main(t[5], t.lineno(1), find_column(input, t.slice[1]))
# --------------------- FUNCTIONS
def p_func_void(t):
    'func : RFUNC ID PARA PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t[2], [], t[6], t.lineno(1), find_column(input, t.slice[1]))
def p_func_params(t) :
    'func     : RFUNC ID PARA params PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))
# params to functions
def p_params_params(t):
    'params : params COMA param'
    t[1].append(t[3])
    t[0] = t[1]
def p_params_param(t):
    'params : param'
    t[0] = [t[1]]
def p_param(t) :
    'param : tipo ID'
    t[0] = {'tipo':t[1],'identificador':t[2]}
def p_tipo(t) :
    '''tipo     : RINT
                | RDOUBLE
                | RSTRING
                | RBOOL
                | RCHAR'''
    if t[1].lower() == 'int':
        t[0] = TIPO.ENTERO
    elif t[1].lower() == 'double':
        t[0] = TIPO.DECIMAL
    elif t[1].lower() == 'string':
        t[0] = TIPO.CADENA
    elif t[1].lower() == 'boolean':
        t[0] = TIPO.BOOLEANO
    elif t[1].lower() == 'char':
        t[0] = TIPO.CHARACTER
def p_return(t) :
    'return     : RRETURN expresion'
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))
# --------------------- CALL FUNCTIONS
def p_llam(t):
    'llam : ID PARA PARC'
    t[0] = Llamada(t[1], [], t.lineno(1), find_column(input, t.slice[1]))
def p_llam_params(t) :
    'llam : ID PARA params_llam PARC'
    t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))
def p_params_llam_1(t):
    'params_llam     : params_llam COMA param_llam'
    t[1].append(t[3])
    t[0] = t[1]
def p_parametrosLL_2(t):
    'params_llam : param_llam'
    t[0] = [t[1]]
def p_parametroLL(t) :
    'param_llam     : expresion'
    t[0] = t[1]
# ///////////////////////////////////////EXPRESION//////////////////////////////////////////////////
def p_expresion_unaria(t):
    '''expresion : MENOS expresion %prec UMENOS
            | NOT expresion %prec UNOT 
    '''
    if t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2], None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2], None, t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
			| expresion DIV expresion
			| expresion POT expresion
			| expresion MOD expresion
            | expresion MENOR expresion
			| expresion MAYOR expresion
			| expresion MENIGUAL expresion
            | expresion MAYIGUAL expresion
			| expresion IGUALIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion OR expresion
			| expresion AND expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENOR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYOR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '=!':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
def p_expresion_agrupacion(t):
    'expresion : PARA expresion PARC'
    t[0] = t[2]
def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(TIPO.ENTERO, t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.CADENA, t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_char(t):
    '''expresion : CHAR'''
    t[0] = Primitivos(TIPO.CHARACTER, t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_nulo(t):
    'expresion : RNULL'
    t[0] = Primitivos(TIPO.NULO, t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_bool_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_bool_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_incremento_decremento(t):
    '''expresion : incremento
                 | decremento'''
    t[0] = t[1]
def p_expresion_llamada(t):
    '''expresion : llam'''
    t[0] = t[1]


def p_expresion_read(t):
    '''expresion : RREAD PARA PARC'''
    t[0] = Read(t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_cast(t):
    '''expresion : PARA tipo PARC expresion'''
    t[0] = Casteo(t[2],t[4],t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_Arreglo(t):
    '''expresion : ID lista_expresiones'''
    t[0] = AccesoArr(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))
# --------------- fin --------------
def p_fin(t):
    '''
    fin : PTCOMA
        | 
    '''

'''def p_error(t):
    if t:
        parser.errok()
    else:
        print("Error EOF")'''
import ply.yacc as yacc

parser = yacc.yacc()

input = ''


def getErrores():
    return errores

def parse(inp):
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

from Nativas.Truncate import Truncate
from Nativas.ToUpper import ToUpper
from Nativas.ToLower import ToLower
from Nativas.TypeOf import TypeOf
from Nativas.Length import Length
from Nativas.Round import Round

def crearNativas(ast):
    nombre = "toupper"
    params = [{'tipo':TIPO.CADENA,'identificador':'$toUpper_param'}]
    instrucciones = []
    toUpper = ToUpper(nombre, params, instrucciones,-1,-1)
    ast.addFuncion(toUpper)  # Guardar la funcion en memoria

    nombre = "tolower"
    params = [{'tipo': TIPO.CADENA, 'identificador': '$toLower_param'}]
    instrucciones = []
    toLower = ToLower(nombre, params, instrucciones, -1, -1)
    ast.addFuncion(toLower)  # Guardar la funcion en memoria

    nombre = "length"
    params = [{'tipo': TIPO.NULO, 'identificador': '$length_param'}]
    instrucciones = []
    length = Length(nombre, params, instrucciones, -1, -1)
    ast.addFuncion(length)  # Guardar la funcion en memoria

    nombre = "truncate"
    params = [{'tipo': TIPO.ENTERO, 'identificador': '$truncate_param'},
              {'tipo': TIPO.DECIMAL, 'identificador': '$truncate_param'}]
    instrucciones = []
    truncate = Truncate(nombre, params, instrucciones, -1, -1)
    ast.addFuncion(truncate)  # Guardar la funcion en memoria

    nombre = "round"
    params = [{'tipo': TIPO.ENTERO, 'identificador': '$round_param'},
              {'tipo': TIPO.DECIMAL, 'identificador': '$round_param'}]
    instrucciones = []
    round = Round(nombre, params, instrucciones, -1, -1)
    ast.addFuncion(round)  # Guardar la funcion en memoria

    nombre = "typeof"
    params = [{'tipo': TIPO.NULO, 'identificador': '$typeof_param'}]
    instrucciones = []
    typeof = TypeOf(nombre, params, instrucciones, -1, -1)
    ast.addFuncion(typeof)  # Guardar la funcion en memoria

from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos
ast = ""
active = False
infTS = {}
def generateCode(entrada):
    global ast
    if entrada != "":
        infTS.clear()
        instrucciones = parse(entrada)  # ARBOL AST
        ast = Arbol(instrucciones)
        TSGlobal = TablaSimbolos()
        ast.setTSglobal(TSGlobal)
        crearNativas(ast)
        for error in errores:  # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
            ast.getExcepciones().append(error)
            ast.updateConsola(error.toString())

        for instruccion in ast.getInstrucciones():  # 1ERA PASADA (DECLARACIONES Y ASIGNACIONES)
            # save functions
            if isinstance(instruccion, Funcion):
                ast.addFuncion(instruccion)
            if isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, ModificarArr)or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion):
                if isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, Declaracion)or isinstance(instruccion, DeclaracionArr2):
                    infTS[instruccion.identificador.lower()+str(TSGlobal)] = ["Global",instruccion.identificador,None,None,None,instruccion.fila,instruccion.columna]
                value = instruccion.interpretar(ast, TSGlobal)
                if isinstance(value, Excepcion):
                    ast.getExcepciones().append(value)
                    ast.updateConsola(value.toString())
                if isinstance(value, Break):
                    err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())

        for instruccion in ast.getInstrucciones():  # 2DA PASADA (MAIN)
            contador = 0
            if isinstance(instruccion, Main):
                contador += 1
                if contador == 2:  # VERIFICAR LA DUPLICIDAD
                    err = Excepcion("Semantico", "Existen 2 funciones Main", instruccion.fila, instruccion.columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())
                    break
                value = instruccion.interpretar(ast, TSGlobal)
                if isinstance(value, Excepcion):
                    ast.getExcepciones().append(value)
                    ast.updateConsola(value.toString())
                if isinstance(value, Break):
                    err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())

        for instruccion in ast.getInstrucciones():  # 3ERA PASADA (SENTENCIAS FUERA DE MAIN)
            if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion,Asignacion) or isinstance(instruccion, Funcion) or isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, ModificarArr)):
                err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
        for error in ast.getExcepciones():
            listExceptions.append(error)
        return ast.getConsola()
# ------------------------------------- DEBUG
debug = False
instrucciones = ""
TSGlobal = TablaSimbolos()
nuevaTabla = TablaSimbolos()  # test main
countDebug = 0
def activeDebug(entrada):
    global debug, instrucciones, ast, TSGlobal, nuevaTabla
    debug = True
    if entrada != "":
        instrucciones = parse(entrada)  # ARBOL AST
        ast = Arbol(instrucciones)
        TSGlobal = TablaSimbolos()
        nuevaTabla = TablaSimbolos()
        ast.setTSglobal(TSGlobal)
        crearNativas(ast)
        for error in errores:  # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
            ast.getExcepciones().append(error)
            ast.updateConsola(error.toString())

        for instruccion in ast.getInstrucciones():  # 3ERA PASADA (SENTENCIAS FUERA DE MAIN)
            if isinstance(instruccion, Funcion):  # save functions
                ast.addFuncion(instruccion)
            if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion,Asignacion) or isinstance(instruccion, Funcion) or isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, ModificarArr)):
                err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
rowDebug = 0
nuevaTablaMain = ""
instruccion = ""
instMain = ""
main = ""
def debuggear(entrada):
    global countDebug, debug, rowDebug, main, instruccion, instMain, nuevaTablaMain, TSGlobal
    if debug:
        if isinstance(instMain, Main) and len(instrucciones)==0:
            # 2DA PASADA ---------------------- EJECT MAIN ------------------
            if len(instMain.instrucciones) != 0:
                inst = instMain.instrucciones.pop(0)
                rowDebug = inst.fila

                if isinstance(inst, Declaracion) or isinstance(inst, DeclaracionArr1) or isinstance(inst, DeclaracionArr2):
                    infTS[inst.identificador.lower() + str(nuevaTablaMain)] = ["Main",
                                                                                          inst.identificador,
                                                                                          None, None, None,
                                                                                          inst.fila,
                                                                                          inst.columna]
                value = inst.interpretar(ast, nuevaTablaMain)
                if isinstance(value, Excepcion):
                    ast.getExcepciones().append(value)
                    ast.updateConsola(value.toString())
                if isinstance(value, Break):
                    err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", inst.fila, inst.columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())
                for error in ast.getExcepciones():
                    listExceptions.append(error)
                countDebug += 1
            else:
                rowDebug = 0
                debug = False
                instruccion = ""
                instMain = ""
        else:
            instruccion = instrucciones.pop(0)
            # 1ERA PASADA (DECLARACIONES Y ASIGNACIONES) --------------
            if isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, ModificarArr)or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion):
                if isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, Declaracion):
                    infTS[instruccion.identificador.lower()+str(TSGlobal)] = ["Global",instruccion.identificador,None,None,None,instruccion.fila,instruccion.columna]
                value = instruccion.interpretar(ast, TSGlobal)

                if isinstance(value, Excepcion):
                    ast.getExcepciones().append(value)
                    ast.updateConsola(value.toString())
                if isinstance(value, Break):
                    err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila,
                                    instruccion.columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())
            if isinstance(instruccion, Main):
                instMain = instruccion
                nuevaTablaMain = TablaSimbolos(TSGlobal)
            rowDebug = instruccion.fila
    return ast.getConsola()

def reportTS():
    Reports.createHTML_TS(infTS, "Reporte_TS")
def reportErrors():
    global listExceptions
    list = []
    # SEMANTIC errors
    for error in listExceptions:
        list.append(error.tipo)
        list.append(error.descripcion)
        list.append(str(error.fila))
        list.append(str(error.columna))
    Reports.createHTML(list, "ReporteJPR")
    listExceptions = []
    errores = []

from Abstract.NodoAST import NodoAST
def createAST():
    init = NodoAST("RAIZ")
    inst = NodoAST("INSTRUCCIONES")

    for instruccion in ast.getInstrucciones():
        inst.addNodeChild(instruccion.getNode())
    init.addNodeChild(inst)
    graph = ast.getDot(init)

    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'ast.dot')
    arch = open(direcc, "w+")
    arch.write(graph)
    arch.close()
    os.system('dot -T pdf -o ast.pdf ast.dot')




