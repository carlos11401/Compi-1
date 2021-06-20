'''
gramatica de JPR
'''
from Expresiones.Relacional import Relacional
from TS.Exception import Excepcion
from Reportes import Reportes as Reports

errores = []
listExceptions = []
reservadas = {
    'var': 'RVAR', 'int': 'RINT', 'double': 'RDOUBLE', 'boolean': 'RBOOL', 'char': 'RCHAR', 'string': 'RSTRING',
    'null': 'RNULL',
    'main': 'RMAIN', 'read': 'RREAD', 'print': 'RPRINT', 'continue': 'RCONTINUE', 'return': 'RRETURN', 'new': 'RNEW',
    'lenght': 'RLENGHT', 'truncate': 'RTRUNCATE', 'round': 'RROUND', 'tipeof': 'RTIPEOF', 'func': 'RFUNC',
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
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Incremento import Incremento
from Instrucciones.Decremento import Decremento
from Instrucciones.Asignacion import Asignacion
from Instrucciones.Imprimir import Imprimir
from Instrucciones.Switch import Switch
from Instrucciones.While import While
from Instrucciones.Break import Break
from Instrucciones.Main import Main
from Instrucciones.Case import Case
from Instrucciones.For import For
from Instrucciones.If import If
from Expresiones.Identificador import Identificador
from Expresiones.Primitivos import Primitivos
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Logica import Logica
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
                        | main'''
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
# ----------------- FOR
def p_for(t):
    '''
    sentFor : RFOR PARA initFor PTCOMA expresion PTCOMA actualizacion PARC LLAVEA instrucciones LLAVEC
    '''
    t[0] = For(t[3],t[5],t[7],t[10],t.lineno(2), find_column(input, t.slice[2]))
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
# --------------- SWITCH
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

from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos

def generateCode(entrada):
    if entrada != "":
        instrucciones = parse(entrada)  # ARBOL AST
        ast = Arbol(instrucciones)
        TSGlobal = TablaSimbolos()
        ast.setTSglobal(TSGlobal)
        for error in errores:  # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
            ast.getExcepciones().append(error)
            ast.updateConsola(error.toString())

        for instruccion in ast.getInstrucciones():  # 1ERA PASADA (DECLARACIONES Y ASIGNACIONES)
            if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion):
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
            if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion,Asignacion)):
                err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
        print(ast.getConsola())
        for error in ast.getExcepciones():
            listExceptions.append(error)
        return ast.getConsola()

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
