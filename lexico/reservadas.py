import re
from enum import Enum
 
 
class TipoToken(Enum):
    # Palabras reservadas
    INT        = "INT"
    STRING     = "STRING"
    FLOAT      = "FLOAT"
    LEER       = "LEER"
    IMPRIMIR   = "IMPRIMIR"
    START      = "START"
    END        = "END"
    IF         = "IF"
    FOR        = "FOR"
    ELSE       = "ELSE"
    WHILE      = "WHILE"
 
    # Tipos de datos
    IDENTIFICADOR = "IDENTIFICADOR"
    ENTERO        = "ENTERO"
    LETRA         = "LETRA"
 
    # Operadores aritméticos
    SUMA     = "SUMA"
    RESTA    = "RESTA"
    MULT     = "MULT"
    DIV      = "DIV"
    ASIG     = "ASIG"
 
    # Operadores de comparación / lógicos
    IGUAL    = "IGUAL"
    MENOR    = "MENOR"
    MAYOR    = "MAYOR"
    MENOR_EQ = "MENOR_EQ"
    MAYOR_EQ = "MAYOR_EQ"
    AND      = "AND"
    AND2     = "AND2"
    OR       = "OR"
    OR2      = "OR2"
 
    # Delimitadores
    COMILLA   = "COMILLA"
    COMA      = "COMA"
    PUNTO_CON = "PUNTO_CON"
    PAR_IZQ   = "PAR_IZQ"
    PAR_DER   = "PAR_DER"
    LLAVE_IZQ = "LLAVE_IZQ"
    LLAVE_DER = "LLAVE_DER"
 
    # Especiales
    DESCONOCIDO = "DESCONOCIDO"
    EOF         = "EOF"
 
 
# ---------------------------------------------------------------------------
# Palabras reservadas (es_reservada = True)
# ---------------------------------------------------------------------------
PALABRAS_RESERVADAS = {
    'Int': {
        'tipo': TipoToken.INT,
        'token': 'Int',
        'lexema': 'Int',
        'tk': 'gz',
        'patron': r'^[Gg][anz]$',
        'descripcion': 'Letra G seguida de la letra a, n, z',
    },
    'String': {
        'tipo': TipoToken.STRING,
        'token': 'String',
        'lexema': 'String',
        'tk': 'str',
        'patron': r'^[Zz][a-zA-Z]+$',
        'descripcion': 'Letra z seguida de más letras',
    },
    'float': {
        'tipo': TipoToken.FLOAT,
        'token': 'float',
        'lexema': 'float',
        'tk': 'fl',
        'patron': r'^[Ff][lie\xDF]',
        'descripcion': 'Letra f seguida de la letra l, i, e, ß',
    },
    'leer': {
        'tipo': TipoToken.LEER,
        'token': 'leer',
        'lexema': 'leer',
        'tk': 'les',
        'patron': r'^[Ll][esen]+',
        'descripcion': 'Letra l seguida de la letra e, s, e, n',
    },
    'imprimir': {
        'tipo': TipoToken.IMPRIMIR,
        'token': 'imp',
        'lexema': 'imprimir',
        'tk': 'dru',
        'patron': r'^[Dd][ru]+',
        'descripcion': 'Letra d seguida de la letra r, u',
    },
    'start': {
        'tipo': TipoToken.START,
        'token': 'start',
        'lexema': 'iniciar',
        'tk': 'anf',
        'patron': r'^[Aa][nfang]+',
        'descripcion': 'Letra a seguida de n, f, a, n, g, e, n',
    },
    'end': {
        'tipo': TipoToken.END,
        'token': 'end',
        'lexema': 'terminar',
        'tk': 'end',
        'patron': r'^[Ee][nde]+',
        'descripcion': 'Letra e seguida de n, d, e',
    },
    'if': {
        'tipo': TipoToken.IF,
        'token': 'if',
        'lexema': 'if',
        'tk': 'wen',
        'patron': r'^[Ww][enn]+',
        'descripcion': 'Letra w seguida de e, n, n',
    },
    'for': {
        'tipo': TipoToken.FOR,
        'token': 'for',
        'lexema': 'for',
        'tk': 'fur',
        'patron': r'^[Ff][\xFCr]+',
        'descripcion': 'Letra f seguida de ü, r',
    },
    'else': {
        'tipo': TipoToken.ELSE,
        'token': 'else',
        'lexema': 'else',
        'tk': 'son',
        'patron': r'^[Ss][onst]+',
        'descripcion': 'Letra s seguida de o, n, s, t',
    },
    'while': {
        'tipo': TipoToken.WHILE,
        'token': 'while',
        'lexema': 'while',
        'tk': 'war',
        'patron': r'^[Ww][\xE4hrend]+',
        'descripcion': 'Letra w seguida de ä, h, r, e, n, d',
    },
}
 
# ---------------------------------------------------------------------------
# Tipos de datos (es_reservada = False)
# ---------------------------------------------------------------------------
TIPOS_DATOS = {
    'identificador': {
        'tipo': TipoToken.IDENTIFICADOR,
        'token': 'Identificador',
        'tk': 'bez',
        'patron': r'^[a-zA-Z][a-zA-Z0-9]*$',
        'descripcion': 'Letra seguida de letra o dígito',
        'reservada': False,
    },
    'entero': {
        'tipo': TipoToken.ENTERO,
        'token': 'entero',
        'tk': 'gan',
        'patron': r'^[1-9][0-9]*$',
        'descripcion': 'Dígito seguido de más dígitos',
        'reservada': False,
    },
    'letra': {
        'tipo': TipoToken.LETRA,
        'token': 'letra',
        'tk': 'buc',
        'patron': r'^[a-zA-Z]+$',
        'descripcion': 'Letra seguida de más letras',
        'reservada': False,
    },
}
 
# ---------------------------------------------------------------------------
# Operadores aritméticos / delimitadores (es_reservada = True)
# ---------------------------------------------------------------------------
OPERADORES_SIMPLES = {
    '+':  {'tipo': TipoToken.SUMA,      'token': '+',  'tk': '+',   'descripcion': 'Signo +'},
    '-':  {'tipo': TipoToken.RESTA,     'token': '-',  'tk': '-',   'descripcion': 'Signo -'},
    '*':  {'tipo': TipoToken.MULT,      'token': '*',  'tk': '*',   'descripcion': 'Signo *'},
    '/':  {'tipo': TipoToken.DIV,       'token': '/',  'tk': '/',   'descripcion': 'Signo /'},
    '=':  {'tipo': TipoToken.ASIG,      'token': '=',  'tk': '=',   'descripcion': 'Signo ='},
    '<':  {'tipo': TipoToken.MENOR,     'token': '<',  'tk': '<',   'descripcion': 'Signo <'},
    '>':  {'tipo': TipoToken.MAYOR,     'token': '>',  'tk': '>',   'descripcion': 'Signo >'},
    '"':  {'tipo': TipoToken.COMILLA,   'token': '"',  'tk': '"',   'descripcion': 'Signo "'},
    ',':  {'tipo': TipoToken.COMA,      'token': ',',  'tk': ',',   'descripcion': 'Signo ,'},
    ';':  {'tipo': TipoToken.PUNTO_CON, 'token': ';',  'tk': ';',   'descripcion': 'Signo ;'},
    '(':  {'tipo': TipoToken.PAR_IZQ,   'token': '(',  'tk': '(',   'descripcion': 'Signo ('},
    ')':  {'tipo': TipoToken.PAR_DER,   'token': ')',  'tk': ')',   'descripcion': 'Signo )'},
    '{':  {'tipo': TipoToken.LLAVE_IZQ, 'token': '{',  'tk': '{',   'descripcion': 'Signo {'},
    '}':  {'tipo': TipoToken.LLAVE_DER, 'token': '}',  'tk': '}',   'descripcion': 'Signo }'},
}
 
 
# ===========================================================================
# Clase Token
# ===========================================================================
class Token:
 
    def __init__(self, tipo, lexema, tk=None, linea=1, columna=1, es_reservada=False):
        self.tipo = tipo
        self.lexema = lexema
        self.tk = tk
        self.linea = linea
        self.columna = columna
        self.es_reservada = es_reservada
 
    def __repr__(self):
        return (
            f"Token(tipo={self.tipo.value}, lexema='{self.lexema}', "
            f"tk='{self.tk}', lin={self.linea}, col={self.columna})"
        )
 
    def __str__(self):
        reservada_str = " [RESERVADA]" if self.es_reservada else ""
        return (
            f"{self.lexema:<15} {self.tipo.value:<15} "
            f"{str(self.tk):<10} L{self.linea}:C{self.columna}{reservada_str}"
        )
 
    def to_dict(self):
        return {
            'tipo': self.tipo.value,
            'lexema': self.lexema,
            'tk': self.tk,
            'linea': self.linea,
            'columna': self.columna,
            'es_reservada': self.es_reservada,
        }
 
 
# ===========================================================================
# Clase ErrorLexico
# ===========================================================================
class ErrorLexico:
 
    def __init__(self, tipo_error, lexema, linea, columna, mensaje):
        self.tipo_error = tipo_error
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.mensaje = mensaje
 
    def __str__(self):
        return (
            f"Error léxico [L{self.linea}:C{self.columna}] "
            f"{self.tipo_error}: {self.mensaje}"
        )
 
    def __repr__(self):
        return (
            f"ErrorLexico({self.tipo_error}, '{self.lexema}', "
            f"L{self.linea}:C{self.columna})"
        )
 
 
# ===========================================================================
# Utilidad: listar palabras reservadas
# ===========================================================================
def listar_palabras_reservadas():
    """Imprime en consola una tabla con todas las palabras reconocidas."""
    sep = "-" * 90
    print(sep)
    print(f"{'TOKEN':<20} {'LEXEMA':<15} {'TK':<8} {'RESERVADA':<10} DESCRIPCIÓN")
    print(sep)
 
    # Palabras reservadas
    for clave, info in PALABRAS_RESERVADAS.items():
        print(
            f"{info['token']:<20} {info['lexema']:<15} {info['tk']:<8} "
            f"{'Sí':<10} {info['descripcion']}"
        )
 
    print(sep)
 
    # Tipos de datos
    for clave, info in TIPOS_DATOS.items():
        print(
            f"{info['token']:<20} {clave:<15} {info['tk']:<8} "
            f"{'No':<10} {info['descripcion']}"
        )
 
    print(sep)
 
    # Operadores simples
    for simbolo, info in OPERADORES_SIMPLES.items():
        print(
            f"{info['token']:<20} {simbolo:<15} {info['tk']:<8} "
            f"{'Sí':<10} {info['descripcion']}"
        )
 
    print(sep)
 
 
# ===========================================================================
# Analizador Léxico
# ===========================================================================
class AnalizadorLexico:
 
    def __init__(self):
        self.tokens: list[Token] = []
        self.errores: list[ErrorLexico] = []
        self.linea_actual = 1
        self.columna_actual = 1
 
    # ------------------------------------------------------------------
    # Helpers de reconocimiento
    # ------------------------------------------------------------------
    def es_palabra_reservada(self, palabra: str):
        """Retorna el dict de la palabra reservada o None.
        Busca tanto en las claves como en los tokens cortos (tk).
        También reconoce variantes comunes."""
        # Primero busca en las claves (ej. 'start', 'end', 'if')
        for clave, info in PALABRAS_RESERVADAS.items():
            if palabra.lower() == clave.lower():
                return info
        
        # Luego busca en los tokens cortos (ej. 'anf', 'end', 'wen')
        for clave, info in PALABRAS_RESERVADAS.items():
            if palabra.lower() == info['tk'].lower():
                return info
        
        # Variantes comunes/alternativas
        variantes = {
            'anb': 'start',    # anb es variante de anf
            'anf': 'start',    # anf es el token corto de start
        }
        
        if palabra.lower() in variantes:
            clave = variantes[palabra.lower()]
            return PALABRAS_RESERVADAS.get(clave, None)
        
        return None
 
    def es_tipo_dato(self, lexema: str):
        """Determina el tipo de dato no-reservado de un lexema."""
        for clave, info in TIPOS_DATOS.items():
            if re.match(info['patron'], lexema):
                return info
        return None
 
    def es_operador_simple(self, simbolo: str):
        """Retorna info del operador/delimitador simple o None."""
        return OPERADORES_SIMPLES.get(simbolo, None)
 
    # ------------------------------------------------------------------
    # Tokenización básica
    # ------------------------------------------------------------------

    # Ya no se usa es_parecida_a_reservada, ahora solo se aceptan tokens exactos

    def tokenizar(self, fuente: str) -> list[Token]:
            self.tokens = []
            self.errores = []
            self.linea_actual = 1
            self.columna_actual = 1
            i = 0
            n = len(fuente)

            while i < n:
                ch = fuente[i]

                # 1. Ignorar espacios y saltos (esto se queda igual)
                if ch == '\n':
                    self.linea_actual += 1
                    self.columna_actual = 1
                    i += 1
                    continue
                if ch in (' ', '\t', '\r'):
                    self.columna_actual += 1
                    i += 1
                    continue

                col_inicio = self.columna_actual

                # 2.a. Cadenas entre dobles comillas: "..."
                if ch == '"':
                    j = i + 1
                    valor = ''
                    cerrado = False
                    while j < n:
                        if fuente[j] == '"':
                            cerrado = True
                            break
                        # Soportar secuencias de escape simples: \" \\ \n \t \r
                        if fuente[j] == '\\' and j + 1 < n:
                            esc = fuente[j+1]
                            if esc == 'n':
                                valor += '\n'
                            elif esc == 't':
                                valor += '\t'
                            elif esc == 'r':
                                valor += '\r'
                            else:
                                valor += esc
                            j += 2
                            continue
                        valor += fuente[j]
                        j += 1

                    if not cerrado:
                        # Error: cadena no cerrada
                        resto = fuente[i: min(n, i+20)]
                        self.errores.append(ErrorLexico("CADENA_NO_CERRADA", resto, self.linea_actual, col_inicio, 'Cadena no cerrada (falta ")'))
                        # Consumimos hasta EOF
                        j = n
                    else:
                        # Consumimos también la comilla de cierre
                        j += 1
                        info_td = TIPOS_DATOS['letra']
                        tok = Token(info_td['tipo'], valor, info_td['tk'], self.linea_actual, col_inicio)
                        self.tokens.append(tok)
                        self.columna_actual += (j - i)
                        i = j
                        continue

                # 2. PRIORIDAD: BLOQUES DE LETRAS (Palabras reservadas o Identificadores)
                # Esto evita que se validen letra por letra
                if ch.isalpha() or ch == '_':
                    j = i
                    while j < n and (fuente[j].isalnum() or fuente[j] == '_'):
                        j += 1
                    lexema = fuente[i:j]
                    
                    # Ahora evaluamos el bloque completo
                    info_res = self.es_palabra_reservada(lexema)
                    if info_res:
                        tok = Token(
                            tipo=info_res['tipo'],
                            lexema=lexema, # Aquí usas el lexema tal cual (ej. 'anf')
                            tk=info_res['tk'],
                            linea=self.linea_actual,
                            columna=col_inicio,
                            es_reservada=True,
                        )
                    else:
                        # Si no es reservada, vemos si es un identificador válido
                        info_td = self.es_tipo_dato(lexema)
                        if info_td:
                            tok = Token(
                                tipo=info_td['tipo'],
                                lexema=lexema,
                                tk=info_td['tk'],
                                linea=self.linea_actual,
                                columna=col_inicio,
                                es_reservada=False,
                            )
                        else:
                            # Si no es ninguna, ahora sí es un error de bloque
                            tok = Token(TipoToken.DESCONOCIDO, lexema, None, self.linea_actual, col_inicio)
                            self.errores.append(ErrorLexico("TOKEN_DESCONOCIDO", lexema, self.linea_actual, col_inicio, f"Lexema '{lexema}' no reconocido"))

                    self.tokens.append(tok)
                    self.columna_actual += (j - i)
                    i = j
                    continue

                # 3. Operadores dobles (==, <=, etc.)
                if i + 1 < n:
                    doble = fuente[i:i+2]
                    if doble in ('==', '<=', '>=', '&&', '||'):
                        from lexico.Oplogicos import OPERADORES_LOGICOS
                        info = OPERADORES_LOGICOS.get(doble)
                        tok = Token(info['tipo'], doble, info['tk'], self.linea_actual, col_inicio, True)
                        self.tokens.append(tok)
                        self.columna_actual += 2
                        i += 2
                        continue

                # 4. Operadores simples (+, -, =, etc.)
                info_op = self.es_operador_simple(ch)
                if info_op:
                    tok = Token(info_op['tipo'], ch, info_op['tk'], self.linea_actual, col_inicio, True)
                    self.tokens.append(tok)
                    self.columna_actual += 1
                    i += 1
                    continue

                # 5. Números (Bloque de dígitos)
                if ch.isdigit():
                    j = i
                    while j < n and fuente[j].isdigit():
                        j += 1
                    lexema = fuente[i:j]
                    info_td = TIPOS_DATOS['entero']
                    tok = Token(info_td['tipo'], lexema, info_td['tk'], self.linea_actual, col_inicio)
                    self.tokens.append(tok)
                    self.columna_actual += (j - i)
                    i = j
                    continue

                # 6. Si nada de lo anterior funcionó, es un caracter realmente inválido (ej. @, $, #)
                self.errores.append(ErrorLexico("CARACTER_INVALIDO", ch, self.linea_actual, col_inicio, f"Carácter '{ch}' no válido"))
                self.tokens.append(Token(TipoToken.DESCONOCIDO, ch, None, self.linea_actual, col_inicio))
                self.columna_actual += 1
                i += 1

            self.tokens.append(Token(TipoToken.EOF, '', 'EOF', self.linea_actual, self.columna_actual))
            return self.tokens
 
    # ------------------------------------------------------------------
    # Reporte
    # ------------------------------------------------------------------
    def imprimir_tokens(self):
        sep = "-" * 70
        print(sep)
        print(f"{'LEXEMA':<15} {'TIPO':<15} {'TK':<10} POSICIÓN")
        print(sep)
        for tok in self.tokens:
            print(tok)
        print(sep)
 
    def imprimir_errores(self):
        if not self.errores:
            print("Sin errores léxicos.")
            return
        print("\n=== ERRORES LÉXICOS ===")
        for err in self.errores:
            print(err)